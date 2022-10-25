from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Used for handling error sequence when desired resource
    is not found.

    Parameters
    ------
    error - Error message
    """
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Used for handling internal error, when a
    user request cannot be processsed correctly
    internally.

    Parameters
    ------
    error - Error message
    """
    db.session.rollback()
    return render_template('errors/500.html'), 500