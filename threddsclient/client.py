import requests

import logging
logger = logging.getLogger(__name__)


def download_urls(url, skip=None, **kwargs):
    return read_url(url, skip, **kwargs).download_urls()


def opendap_urls(url, skip=None, **kwargs):
    return read_url(url, skip, **kwargs).opendap_urls()


def read_url(url, skip=None, **kwargs):
    """
    Create a Catalog from a Thredds catalog link

    :param str url:     URL pointing to a Thredds catalog.xml file
    :param \**kwargs:   Arguments to pass to requests.get()
                        (e.g. for authentication)
    :rtype Catalog

    :raises ValueError: if the XML is not a Thredds catalog
    :raises requests.ConnectionError: if unable to connect to the URL
    """
    req = requests.get(url, **kwargs)
    return read_xml(req.text, url)


def read_xml(xml, baseurl, skip=None):
    """
    Create a Catalog from a XML string

    :param str xml:     XML code for a Thredds catalog
    :param str baseurl: URL base to use for catalog links
    :param str skip:        list of dataset names and/or a catalogRef titles.  Python regex supported.
    :rtype Catalog

    :raises ValueError: if the XML is not a Thredds catalog
    """
    from bs4 import BeautifulSoup as BSoup
    from .catalog import Catalog
    
    try:
        soup = BSoup(xml, 'xml').catalog
        soup.name  # Xml should contain <catalog/> at top level
    except AttributeError:
        raise ValueError("Does not appear to be a Thredds catalog")

    return Catalog(soup, baseurl, skip)
