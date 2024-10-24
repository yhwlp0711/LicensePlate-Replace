from __future__ import print_function

import argparse

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torchvision
import cv2

from data import cfg_mnet, cfg_re50
from layers.functions.prior_box import PriorBox
from models.retina import Retina
from utils.box_utils import decode, decode_landm
from utils.nms.py_cpu_nms import py_cpu_nms

print(torch.__version__, torchvision.__version__)


def getargs():
    parser = argparse.ArgumentParser(description='RetinaPL')
    # 23 good
    parser.add_argument('-m', '--trained_model', default='./weights/mobilenet0.25_epoch_20_ccpd.pth',
                        type=str, help='Trained state_dict file path to open')
    parser.add_argument('--network', default='mobile0.25', help='Backbone network mobile0.25 or resnet50')
    parser.add_argument('--cpu', action="store_true", default=False, help='Use cpu inference')
    parser.add_argument('--confidence_threshold', default=0.02, type=float, help='confidence_threshold')
    parser.add_argument('--top_k', default=1000, type=int, help='top_k')
    parser.add_argument('--nms_threshold', default=0.4, type=float, help='nms_threshold')
    parser.add_argument('--keep_top_k', default=500, type=int, help='keep_top_k')
    parser.add_argument('-s', '--save_image', action="store_true", default=True, help='show detection results')
    parser.add_argument('--vis_thres', default=0.75, type=float, help='visualization_threshold')
    # parser.add_argument('-image', default='test_images/0.jpg', help='test image path')
    args = parser.parse_args()
    return args


def check_keys(model, pretrained_state_dict):
    ckpt_keys = set(pretrained_state_dict.keys())
    model_keys = set(model.state_dict().keys())
    used_pretrained_keys = model_keys & ckpt_keys
    unused_pretrained_keys = ckpt_keys - model_keys
    missing_keys = model_keys - ckpt_keys
    print('Missing keys:{}'.format(len(missing_keys)))
    print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
    print('Used keys:{}'.format(len(used_pretrained_keys)))
    assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
    return True


def remove_prefix(state_dict, prefix):
    """ Old style model is stored with all names of parameters sharing common prefix 'module.' """
    print('remove prefix \'{}\''.format(prefix))
    f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
    return {f(key): value for key, value in state_dict.items()}


def load_model(model, pretrained_path, load_to_cpu):
    print('Loading pretrained model from {}'.format(pretrained_path))
    if load_to_cpu:
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
    else:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage.cuda(device))
    if "state_dict" in pretrained_dict.keys():
        pretrained_dict = remove_prefix(pretrained_dict['state_dict'], 'module.')
    else:
        pretrained_dict = remove_prefix(pretrained_dict, 'module.')
    check_keys(model, pretrained_dict)
    model.load_state_dict(pretrained_dict, strict=False)
    return model


def detect(img_list):
    args = getargs()
    torch.set_grad_enabled(False)
    cfg = None
    if args.network == "mobile0.25":
        cfg = cfg_mnet
    elif args.network == "resnet50":
        cfg = cfg_re50
    # net and model
    net = Retina(cfg=cfg, phase='test')
    # net = load_model(net, args.trained_model, "cuda:0")
    net = load_model(net, args.trained_model, "mps")
    net.eval()
    # print('Finished loading model!')
    # print(net)
    cudnn.benchmark = True
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = torch.device("mps")
    net = net.to(device)

    resize = 1
    pointlist = list()
    # testing begin
    for currentImgs in img_list:
        currentlistpointlist = list()
        for currentImg in currentImgs[1:]:
            # img_raw = cv2.imread(filepath, cv2.IMREAD_COLOR)

            img = np.float32(currentImg)

            im_height, im_width, _ = img.shape
            scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
            img -= (104, 117, 123)
            img = img.transpose(2, 0, 1)
            img = torch.from_numpy(img).unsqueeze(0)
            img = img.to(device)
            scale = scale.to(device)

            loc, conf, landms = net(img)  # forward pass
            # print('net forward time: {:.4f}'.format(time.time() - tic))

            priorbox = PriorBox(cfg, image_size=(im_height, im_width))
            priors = priorbox.forward()
            priors = priors.to(device)
            prior_data = priors.data
            boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
            boxes = boxes * scale / resize
            boxes = boxes.cpu().numpy()

            scores = conf.squeeze(0).data.cpu().numpy()[:, 1]

            landms = decode_landm(landms.data.squeeze(0), prior_data, cfg['variance'])
            scale1 = torch.Tensor([img.shape[3], img.shape[2], img.shape[3], img.shape[2],
                                   img.shape[3], img.shape[2],
                                   img.shape[3], img.shape[2]])
            scale1 = scale1.to(device)
            landms = landms * scale1 / resize
            landms = landms.cpu().numpy()

            # ignore low scores
            inds = np.where(scores > args.confidence_threshold)[0]
            boxes = boxes[inds]
            landms = landms[inds]
            scores = scores[inds]

            # keep top-K before NMS
            order = scores.argsort()[::-1][:args.top_k]
            boxes = boxes[order]
            landms = landms[order]
            scores = scores[order]

            # do NMS
            dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
            keep = py_cpu_nms(dets, args.nms_threshold)
            # keep = nms(dets, args.nms_threshold,force_cpu=args.cpu)
            dets = dets[keep, :]
            landms = landms[keep]

            # keep top-K faster NMS
            dets = dets[:args.keep_top_k, :]
            landms = landms[:args.keep_top_k, :]

            dets = np.concatenate((dets, landms), axis=1)
            # print('priorBox time: {:.4f}'.format(time.time() - tic))
            # show image
            currentpointlist = list()
            for b in dets:
                if b[4] < args.vis_thres:
                    continue
                b = list(map(int, b))
                rightdown = (b[5], b[6])
                leftdown = (b[7], b[8])
                leftup = (b[9], b[10])
                rightup = (b[11], b[12])
                currentpointlist.append((leftup, rightup, leftdown, rightdown))
            # 绘制车牌区域
            # for point in currentpointlist:
            #     cv2.rectangle(currentImg, point[0], point[3], (0, 255, 0), 2)
            #     cv2.circle(currentImg, point[0], 2, (0, 0, 255), 2)
            #     cv2.circle(currentImg, point[1], 2, (0, 0, 255), 2)
            #     cv2.circle(currentImg, point[2], 2, (0, 0, 255), 2)
            #     cv2.circle(currentImg, point[3], 2, (0, 0, 255), 2)
            # cv2.imshow('img', currentImg)
            # cv2.waitKey(0)
            currentlistpointlist.append(currentpointlist)
        pointlist.append(currentlistpointlist)
    return pointlist

# import cv2

# if __name__ == '__main__':
#     img = cv2.imread('./testimgs/3.jpg')
#     # cv2.imshow('img', img)
#     # cv2.waitKey(0)
#     res = detect([[0, img]])
#     print(res)