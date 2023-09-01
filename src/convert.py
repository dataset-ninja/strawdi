# https://strawdi.github.io/

import os
import shutil
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
from cv2 import connectedComponents
from dotenv import load_dotenv
from tqdm import tqdm

import src.settings as s
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "StrawDI"
    dataset_path = "/home/alex/DATASETS/TODO/StrawDI/StrawDI_Db1"
    ds_name = "ds"
    images_folder = "img"
    masks_folder = "label"
    images_shape = (1296, 966)
    batch_size = 3

    def create_ann(im_path):
        mask_path = os.path.join(masks_path, get_file_name_with_ext(im_path))
        ann_np = sly.imaging.image.read(mask_path)[:, :, 0]
        unique_idx = list(np.unique(ann_np))
        unique_idx.remove(0)
        labels = []
        for idx in unique_idx:
            mask = ann_np == idx
            curr_bitmap = sly.Bitmap(mask)
            curr_label = sly.Label(curr_bitmap, obj_class)
            labels.append(curr_label)

        return sly.Annotation(img_size=(ann_np.shape[0], ann_np.shape[1]), labels=labels)

    obj_class_name = "strawberry"
    obj_class = sly.ObjClass(obj_class_name, sly.Bitmap)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(obj_classes=[obj_class])
    api.project.update_meta(project.id, meta.to_json())

    for ds_name in os.listdir(dataset_path):
        curr_folder_path = os.path.join(dataset_path, ds_name)
        if dir_exists(curr_folder_path):
            dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

            images_path = os.path.join(curr_folder_path, images_folder)
            masks_path = os.path.join(curr_folder_path, masks_folder)
            images_names = os.listdir(images_path)

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_path_batch = [
                    os.path.join(images_path, image_name) for image_name in images_names_batch
                ]

                img_infos = api.image.upload_paths(
                    dataset.id, images_names_batch, images_path_batch
                )
                img_ids = [im_info.id for im_info in img_infos]

                anns_batch = [create_ann(image_path) for image_path in images_path_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(images_path_batch))
    return project
