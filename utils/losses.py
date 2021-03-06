import torch
import torch.nn as nn
import torch.nn.functional as F


class Loss:
    def __init__(self, cls_factor=1, box_factor=1, landmark_factor=1):
        self.cls_factor = cls_factor
        self.box_factor = box_factor
        self.land_factor = landmark_factor
        self.loss_cls = nn.BCELoss()
        self.loss_box = nn.MSELoss()
        self.loss_landmark = nn.MSELoss()

    def cls_loss(self, gt_label, pred_label):
        pred_label = torch.squeeze(pred_label)
        gt_label = torch.squeeze(gt_label)
        mask = torch.ge(gt_label, 0)
        valid_gt_label = torch.masked_select(gt_label, mask)
        valid_pred_label = torch.masked_select(pred_label, mask)
        return self.loss_cls(valid_pred_label, valid_gt_label) * self.cls_factor

    def box_loss(self, gt_label, gt_offset, pred_offset):
        pred_offset = torch.squeeze(pred_offset)
        gt_offset = torch.squeeze(gt_offset)
        gt_label = torch.squeeze(gt_label)
        unmask = torch.eq(gt_label, 0)
        mask = torch.eq(unmask, 0)
        chose_index = torch.nonzero(mask.data)
        chose_index = torch.squeeze(chose_index)
        valid_gt_offset = gt_offset[chose_index, :]
        valid_pred_offset = pred_offset[chose_index, :]
        if torch.sum(mask) != 0:
           return self.loss_box(valid_pred_offset, valid_gt_offset) * self.box_factor
        else:
           return 0

    def landmark_loss(self, gt_label, gt_landmark, pred_landmark):
        pred_landmark = torch.squeeze(pred_landmark)
        gt_landmark = torch.squeeze(gt_landmark)
        gt_label = torch.squeeze(gt_label)
        mask = torch.eq(gt_label, -2)
        chose_index = torch.nonzero(mask.data)
        chose_index = torch.squeeze(chose_index)
        valid_gt_landmark = gt_landmark[chose_index, :]
        valid_pred_landmark = pred_landmark[chose_index, :]
        if torch.sum(mask) != 0:
           return self.loss_landmark(valid_pred_landmark, valid_gt_landmark) * self.land_factor
        else:
           return 0
