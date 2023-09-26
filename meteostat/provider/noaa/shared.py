from ftplib import FTP


NOAA_NCDC_FTP_SERVER = "ftp.ncdc.noaa.gov"

def get_ftp_connection() -> FTP:
    """
    Get NOAA NCDC FTP connection
    """
    ftp = FTP(NOAA_NCDC_FTP_SERVER)
    ftp.login()
    return ftp
