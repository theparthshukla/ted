#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from zimscraperlib.video.encoding import reencode
from zimscraperlib.imaging import resize_image

from .constants import getLogger


logger = getLogger()


def post_process_video(
    video_dir, video_id, preset, video_format, low_quality, skip_recompress
):
    """apply custom post-processing to downloaded video

    - resize thumbnail
    - recompress video if incorrect video_format or low_quality requested
    """

    # find downloaded video from video_dir
    files = [p for p in video_dir.iterdir() if p.stem == "video" and p.suffix != ".jpg"]
    if len(files) == 0:
        logger.error(f"Video file missing in {video_dir} for {video_id}")
        logger.debug(list(video_dir.iterdir()))
        raise FileNotFoundError(f"Missing video file in {video_dir}")
    if len(files) > 1:
        logger.warning(
            f"Multiple video file candidates for {video_id} in {video_dir}. Picking {files[0]} out of {files}"
        )
    src_path = files[0]

    # resize thumbnail. we use max width:248x187px in listing
    resize_image(
        src_path.parent.joinpath("thumbnail.jpg"),
        width=248,
        height=187,
        method="cover",
    )

    # don't reencode if not requesting low-quality and received wanted format
    if skip_recompress or (not low_quality and src_path.suffix[1:] == video_format):
        return

    dst_path = src_path.parent.joinpath(f"video.{video_format}")
    logger.debug(f"Converting video {video_id}")
    reencode(
        src_path, dst_path, preset.to_ffmpeg_args(), delete_src=True, failsafe=False
    )
