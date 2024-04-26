from swiftai.pipelines.spleen_segment_pipeline import SpleenSegment

def new_job(method, file_in, file_out):

    pipeline = method(
        pipeline_output_dir="experiment_outputs",
        input_image=file_in,
        output_filename=file_out,
        pipeline=None,
        device="cuda:0",
        data_dependencies=None)
    pipeline.run()


methodDict = {"Spleen Segment": SpleenSegment}