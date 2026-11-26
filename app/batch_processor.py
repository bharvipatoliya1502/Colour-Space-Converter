"""FIFO batch jobs with database status transitions."""
from PIL import Image
from db.database import save_image_record, update_image_dimensions, save_colour_space_record, save_conversion_record, update_conversion_status
from math_engine.converter import convert_image_to_yiq, convert_yiq_array_to_rgb, image_difference

def enqueue_batch_file(uploaded_file):
    image_id=save_image_record(uploaded_file.name,None,None,getattr(uploaded_file,"type","Unknown"))
    conversion_id=save_conversion_record(image_id,"Batch RGB to YIQ to RGB",status="queued")
    return {"image_id":image_id,"conversion_id":conversion_id,"file":uploaded_file}

def run_batch_job(job):
    cid=job["conversion_id"]; file=job["file"]
    update_conversion_status(cid,"processing")
    try:
        if hasattr(file,"seek"): file.seek(0)
        image=Image.open(file).convert("RGB"); image.thumbnail((400,400))
        update_image_dimensions(job["image_id"],image.width,image.height)
        yiq,original=convert_image_to_yiq(image); restored=convert_yiq_array_to_rgb(yiq)
        mae,rmse,_=image_difference(original,restored)
        save_colour_space_record(job["image_id"])
        update_conversion_status(cid,"success",mae,rmse)
        return {"status":"success","mae":mae,"rmse":rmse,"error":None}
    except Exception as error:
        update_conversion_status(cid,"failed")
        return {"status":"failed","mae":None,"rmse":None,"error":str(error)}

def process_batch_file(uploaded_file):
    return run_batch_job(enqueue_batch_file(uploaded_file))
