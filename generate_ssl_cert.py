class NginxCert():

  # The path on the local filesystem where we can read and write
  # AppScale deployment metadata.
  LOCAL_NGINX_PATH = "/etc/nginx/"


  @classmethod
  def get_certificate_location(cls, keyname):
    """Determines the location where the self-signed certificate for this
    AppScale deployment can be found.

    Args:
      keyname: A str that indicates the name of the SSH keypair that
        uniquely identifies this AppScale deployment.
    Returns:
      A str that indicates where the self-signed certificate can be found.
    """
    return cls.LOCAL_NGINX_PATH + keyname + "-cert.pem"


  @classmethod
  def get_private_key_location(cls, keyname):
    """Determines the location where the private key used to sign the
    self-signed certificate used for this AppScale deployment can be found.

    Args:
      keyname: A str that indicates the name of the SSH keypair that
        uniquely identifies this AppScale deployment.
    Returns:
      A str that indicates where the private key can be found.
    """
    return cls.LOCAL_NGINX_PATH + keyname + "-key.pem"


  @classmethod
  def generate_ssl_cert(cls, keyname, is_verbose):
    """Generates a self-signed SSL certificate that AppScale services can use
    to encrypt traffic with.

    Args:
      keyname: A str representing the SSH keypair name used for this AppScale
        deployment.
      is_verbose: A bool that indicates if we want to print out the certificate
        generation to stdout or not.
    """
    cls.shell("openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 " + \
      "-subj '/C=US/ST=Foo/L=Bar/O=AppScale/CN=appscale.com' " + \
      "-keyout {0} -out {1}".format(NginxCert.get_private_key_location(keyname),
      NginxCert.get_certificate_location(keyname)), is_verbose, stdin=None)