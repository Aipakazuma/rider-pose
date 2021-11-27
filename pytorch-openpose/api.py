import cv2
import copy
import numpy as np
import torch
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from PIL import Image
from typing import Dict
import uuid
import io

from src import util
from src.body import Body
from src.hand import Hand


def load_models():
    body_estimation = Body('model/body_pose_model.pth')
    hand_estimation = Hand('model/hand_pose_model.pth')
    return {
        'body': body_estimation,
        'hand': hand_estimation
    }


def write_post_movie(body):
    with open('./video.webm', 'wb') as f:
        f.write(body)


def read_video():
    models = load_models()
    cap = cv2.VideoCapture('./video.webm')
    results_img = []
    results_point = []
    while cap.isOpened():
        ret, ori_img = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB)
        canvas, candidate, subset = detect(img, models)
        results_img.append(canvas)

        r = detect_point_to_array(candidate, subset)
        results_point.append(r)

    cap.release()
    cv2.destroyAllWindows()

    return results_img, results_point


def detect_point_to_array(candidate, subset):
    results = [[0, 0] for _ in range(18)]
    for class_idx, candidate_index in enumerate(subset[0][:17]):
        candidate_index = int(candidate_index)
        if candidate_index == -1:
            continue
        x, y = candidate[candidate_index][0:2]
        results[class_idx] = [x, y]

    return results


def detect(img, models):
    candidate, subset = models['body'](img)
    canvas = copy.deepcopy(img)
    canvas = util.draw_bodypose(canvas, candidate, subset)

    # detect hand
    # hands_list = util.handDetect(candidate, subset, img)
    # all_hand_peaks = []
    # for x, y, w, _ in hands_list:
    #     peaks = models['hand'](img[y:y+w, x:x+w, :])
    #     peaks[:, 0] = np.where(
    #         peaks[:, 0] == 0, peaks[:, 0],
    #         peaks[:, 0]+x)
    #     peaks[:, 1] = np.where(
    #         peaks[:, 1] == 0, peaks[:, 1],
    #         peaks[:, 1]+y)
    #     all_hand_peaks.append(peaks)

    # canvas = util.draw_handpose(canvas, all_hand_peaks)
    return canvas, candidate, subset


def create_animation_gif(imgs, random_str):
    new_imgs = [Image.fromarray(img) for img in imgs]
    new_imgs[0].save('output_{}.gif'.format(random_str),
                     save_all=True,
                     append_images=new_imgs[1:],
                     optimize=False,
                     duration=300,
                     loop=0)


def main(body, random_str):
    try:
        print(f"Torch device: {torch.cuda.get_device_name()}")
    except Exception as e:
        print(e)

    write_post_movie(body)
    results_img, results_point = read_video()
    create_animation_gif(results_img, random_str)
    print(np.array(results_point))


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


class Task():
    def __init__(self, body, job_id):
        self.body = body
        self.job_id = job_id
        self.random_str = '{}_{}'.format(self.job_id, str(uuid.uuid4()))

    def __call__(self):
        jobs[self.job_id] = self
        try:
            main(self.body, self.random_str)
            done_jobs[self.job_id] = self.random_str
        except Exception as e:
            print(e)

        del jobs[self.job_id]


jobs: Dict[int, Task] = {}
done_jobs: Dict[int, str] = {}


@app.get('/video')
async def job_list():
    job_ids = [job_id for job_id, _ in jobs.items()]
    return {"job_ids": job_ids}


@app.get('/video/{job_id}')
async def status_check(job_id: int):
    return {"status": job_id in jobs}


@app.get('/video/output/{job_id}')
def get_gif(job_id: int):
    if job_id not in done_jobs:
        return None

    t = done_jobs[job_id]
    file_name = './output_{}.gif'.format(t)
    with open(file_name, 'rb') as f:
        results = f.read()

    print(file_name)
    return StreamingResponse(io.BytesIO(results), media_type="image/gif")


@app.post('/video/{job_id}')
def post_video(background_tasks: BackgroundTasks,
               job_id: int,
               video_data: UploadFile = File(...)):
    body = video_data.file.read()
    t = Task(body, job_id)
    background_tasks.add_task(t)
    return {
        "upload_file_size": len(body),
        "job_id": job_id
    }
