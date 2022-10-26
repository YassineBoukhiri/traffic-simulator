from fastapi import APIRouter
from model import Model
from video_processor import get_traffic_density

router = APIRouter(prefix='/traffic', tags=['traffic-state'])

@router.post('/')
def post_traffic_state(input_data: Model):
    """
    :param input_data: input data
    :return: traffic density per lane
    """
    print({"id_camera": input_data.camera_id, "traffic_density": [{"way": 1, "density": get_traffic_density(input_data).name}], "timestamp": input_data.timestamp})