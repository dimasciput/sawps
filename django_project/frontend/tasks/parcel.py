from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(name="clear_uploaded_boundary_files")
def clear_uploaded_boundary_files():
    from datetime import datetime, timedelta
    from frontend.models.boundary_search import BoundaryFile
    datetime_filter = datetime.now() - timedelta(days=90)
    old_files = BoundaryFile.objects.filter(
        upload_date__lt=datetime_filter
    )
    old_files.delete()


@shared_task(name='boundary_files_search')
def boundary_files_search(request_id):
    from frontend.models.boundary_search import BoundarySearchRequest
    from frontend.utils.upload_file import search_parcels_by_boundary_files
    search_request = BoundarySearchRequest.objects.get(id=request_id)
    search_parcels_by_boundary_files(search_request)
