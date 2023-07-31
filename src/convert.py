import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import dir_exists, get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/StrawDI/StrawDI_Db1"
    ds_name = "ds"
    images_folder = "img"
    masks_folder = "label"
    batch_size = 30

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
    obj_class = sly.ObjClass(obj_class_name, sly.Bitmap, color=(255, 0, 0))

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
