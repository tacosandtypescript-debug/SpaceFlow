class SpaceFlowError(Exception):
    """Error esperado que puede mostrarse directamente al usuario."""


class InvalidSpaceUrl(SpaceFlowError):
    pass


class AuthenticationRequired(SpaceFlowError):
    pass


class SpaceUnavailable(SpaceFlowError):
    pass


class DownloadFailed(SpaceFlowError):
    pass


class PlaybackFailed(SpaceFlowError):
    pass


class UpdateFailed(SpaceFlowError):
    pass
