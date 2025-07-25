import dataclasses
import glob

import flask

import json_response


@dataclasses.dataclass
class LicenseMetadata:
    name: str
    homepage_url: str
    # The license_glob_pattern and license_url properties are mutually
    # exclusive.
    # Glob pattern that points to the license file on the local system.
    license_glob_pattern: str = ''
    # URL of license file if it's not available on the local system.
    license_url: str = ''


# For code where the source or license is on the local device, prefer linking to
# the locally-available copy instead of the remote URL so that the license ties
# tightly to the version we're using. When that's not possible, look for
# permalink versions of the license that match the version of the software we're
# using.

# pylint: disable=line-too-long
_LICENSE_METADATA = [
    LicenseMetadata(name='TinyPilot',
                    license_glob_pattern='./LICENSE',
                    homepage_url='https://tinypilotkvm.com'),
    LicenseMetadata(
        name='uStreamer',
        license_url=
        'https://raw.githubusercontent.com/tiny-pilot/ustreamer/v6.36/LICENSE',
        homepage_url='https://github.com/pikvm/ustreamer'),
    LicenseMetadata(name='Python',
                    homepage_url='https://python.org',
                    license_glob_pattern='/usr/lib/python3.*/LICENSE.txt'),
    LicenseMetadata(name='nginx',
                    license_url='https://nginx.org/LICENSE',
                    homepage_url='https://nginx.org'),
    LicenseMetadata(
        name='Janus',
        homepage_url='https://janus.conf.meetecho.com',
        license_url=
        'https://raw.githubusercontent.com/meetecho/janus-gateway/v1.0.1/COPYING'
    ),

    # JavaScript dependencies.
    LicenseMetadata(
        name='janus.js',
        homepage_url='https://janus.conf.meetecho.com',
        license_glob_pattern='./app/static/third-party/janus-gateway/*/janus.js',
    ),
    LicenseMetadata(
        name='webrtc-adapter',
        homepage_url='https://github.com/webrtcHacks/adapter',
        license_glob_pattern=
        './app/static/third-party/webrtc-adapter/*/adapter.min.js',
    ),
    LicenseMetadata(
        name='socket.io',
        homepage_url='https://socket.io',
        license_url=
        'https://raw.githubusercontent.com/socketio/socket.io/4.7.1/LICENSE',
    ),

    # Python dependencies, from requirements.txt.
    LicenseMetadata(
        name='eventlet',
        homepage_url='https://eventlet.net',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/eventlet-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='Flask',
        homepage_url='https://flask.palletsprojects.com',
        license_url=
        'https://raw.githubusercontent.com/pallets/flask/3.1.1/LICENSE.txt',
    ),
    LicenseMetadata(
        name='Flask-SocketIO',
        homepage_url='https://flask-socketio.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/Flask_SocketIO-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='Flask-WTF',
        homepage_url='https://flask-wtf.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/flask_wtf-*.dist-info/licenses/LICENSE*'
    ),
    LicenseMetadata(
        name='pyyaml',
        homepage_url='https://pyyaml.org',
        # We're unable to consistently link to the local license file because of
        # inconsistent Python package structure.
        # https://github.com/tiny-pilot/tinypilot/issues/1899
        license_url=
        'https://raw.githubusercontent.com/yaml/pyyaml/6.0.2/LICENSE',
    ),
    LicenseMetadata(
        name='bidict',
        homepage_url='https://bidict.readthedocs.io/en/main',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/bidict-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='blinker',
        homepage_url='https://blinker.readthedocs.io/',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/blinker-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='click',
        homepage_url='https://palletsprojects.com/p/click',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/click-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='dnspython',
        homepage_url='https://www.dnspython.org',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/dnspython-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='greenlet',
        homepage_url='https://greenlet.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/greenlet-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='h11',
        homepage_url='https://h11.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/h11-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='importlib-metadata',
        homepage_url='https://importlib-metadata.readthedocs.io/',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/importlib_metadata-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='itsdangerous',
        homepage_url='https://palletsprojects.com/p/itsdangerous/',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/itsdangerous-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='Jinja2',
        homepage_url='https://palletsprojects.com/p/jinja/',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/jinja2-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='MarkupSafe',
        homepage_url='https://palletsprojects.com/p/markupsafe/',
        # We're unable to consistently link to the local license file because of
        # inconsistent Python package structure.
        # https://github.com/tiny-pilot/tinypilot/issues/1899
        license_url=
        'https://raw.githubusercontent.com/pallets/markupsafe/3.0.2/LICENSE.txt',
    ),
    LicenseMetadata(
        name='python-dotenv',
        homepage_url='https://github.com/theskumar/python-dotenv',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/python_dotenv-*.dist-info/licenses/LICENSE',
    ),
    LicenseMetadata(
        name='python-engineio',
        homepage_url='https://github.com/miguelgrinberg/python-engineio',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/python_engineio-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='python-socketio',
        homepage_url='https://github.com/miguelgrinberg/python-socketio',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/python_socketio-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='simple-websocket',
        homepage_url='https://simple-websocket.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/simple_websocket-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='Werkzeug',
        homepage_url='https://palletsprojects.com/p/werkzeug/',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/werkzeug-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='wsproto',
        homepage_url='https://wsproto.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/wsproto-*.dist-info/LICENSE*',
    ),
    LicenseMetadata(
        name='WTForms',
        homepage_url='https://wtforms.readthedocs.io',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/wtforms-*.dist-info/licenses/LICENSE*',
    ),
    LicenseMetadata(
        name='zipp',
        homepage_url='https://github.com/jaraco/zipp',
        license_glob_pattern=
        './venv/lib/python3.*/site-packages/zipp-*.dist-info/licenses/LICENSE*',
    ),

    # Indirect dependencies through Janus.
    LicenseMetadata(
        name='libnice',
        homepage_url='https://gitlab.freedesktop.org/libnice/libnice',
        license_url=
        'https://gitlab.freedesktop.org/libnice/libnice/-/raw/0.1.18/COPYING',
    ),
    LicenseMetadata(
        name='libsrtp',
        homepage_url='https://github.com/cisco/libsrtp',
        license_url=
        'https://raw.githubusercontent.com/cisco/libsrtp/v2.2.0/LICENSE',
    ),
    LicenseMetadata(
        name='libwebsockets',
        homepage_url='https://libwebsockets.org',
        # In the past, we used to link to the license that was hosted on the
        # git mirror at libwebsockets.org/git. We repeatedly experienced
        # outages of their website, however, so for reliability reasons, we now
        # link to Github instead.
        # (See https://github.com/tiny-pilot/tinypilot/pull/1727)
        license_url=
        'https://raw.githubusercontent.com/warmcat/libwebsockets/v3.2.2/LICENSE',
    ),

    # Fonts.
    LicenseMetadata(
        name='Overpass',
        homepage_url='https://overpassfont.org/',
        license_glob_pattern=
        './app/static/third-party/fonts/Overpass-License.txt',
    ),
]

blueprint = flask.Blueprint('licensing', __name__, url_prefix='/licensing')


@blueprint.route('', methods=['GET'])
def all_licensing_get():
    """Retrieves licensing metadata for TinyPilot and its dependencies.

    Returns:
        A JSON-formatted list of licensing information about TinyPilot and its
        third-party dependencies.

        Example:
        [
            {
                "name": "TinyPilot",
                "homepageUrl": "https://tinypilotkvm.com",
                "licenseUrl": "/licensing/TinyPilot/license"
            },
            {
                "name": "uStreamer",
                "homepageUrl": "https://github.com/pikvm/ustreamer",
                "licenseUrl": "/licensing/uStreamer/license"
            },
            ...
        ]
    """
    response = []
    for license_data in _LICENSE_METADATA:
        response.append({
            'name': license_data.name,
            'licenseUrl': f'/licensing/{license_data.name}/license',
            'homepageUrl': license_data.homepage_url,
        })

    return json_response.success(response)


@blueprint.route('/<project>/license', methods=['GET'])
def project_license_get(project):
    """Retrieves the license for a given project.

    Args:
        project: The name of the project's license to retrieve.

    Returns:
        A plaintext response with the license in plaintext if the license is
        available locally, or a redirect to a public URL if the license is not
        available locally.
    """
    project_metadata = _get_project_metadata(project)
    if not project_metadata:
        return flask.make_response('Unknown project', 404)

    if project_metadata.license_url:
        return _make_redirect_response(project_metadata.license_url)

    matches = glob.glob(project_metadata.license_glob_pattern)
    if not matches:
        return flask.make_response('Project license not found', 404)

    license_path = matches[0]
    return _make_plaintext_response(_read_file(license_path))


def _get_project_metadata(project_name):
    for license_data in _LICENSE_METADATA:
        if license_data.name == project_name:
            return license_data
    return None


def _make_plaintext_response(response_body):
    response = flask.make_response(response_body, 200)
    response.mimetype = 'text/plain'
    return response


def _read_file(license_path):
    with open(license_path, encoding='utf-8') as license_file:
        return license_file.read()


def _make_redirect_response(license_url):
    # We intentionally use a 302 temporary redirect, as the license URL will
    # change when software versions change.
    return flask.redirect(license_url, code=302)
