from flask import Blueprint, jsonify, url_for
from cheapflight.models.crawl_job import CrawlJob
from cheapflight.models.price_history import LowestPriceHistory


bp = Blueprint('api', __name__, url_prefix="/api")


@bp.route('/')
def index():
    return jsonify({
        "crawl_jobs": url_for(".crawl_jobs", _external=True),
        "price_history": url_for(".price_history", _external=True)
    })


@bp.route('/crawl_jobs/')
def crawl_jobs():
    return jsonify({
        "status": "ok",
        "response": [job.to_dict() for job in CrawlJob.get_jobs(at=None)]
    })


@bp.route('/price_history/')
def price_history():
    r = LowestPriceHistory.list()
    return jsonify({
        "status": "ok",
        "response": r
    })
