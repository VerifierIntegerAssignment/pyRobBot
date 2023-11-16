import pytest

from pyrobbot.__main__ import main
from pyrobbot.argparse_wrapper import get_parsed_args


def test_default_command():
    args = get_parsed_args(argv=[])
    assert args.command == "voice"


@pytest.mark.usefixtures("_input_builtin_mocker")
@pytest.mark.parametrize("user_input", ["Hi!", ""], ids=["regular-input", "empty-input"])
def test_terminal_command(cli_args_overrides):
    args = ["terminal", "--report-accounting-when-done", *cli_args_overrides]
    args = list(dict.fromkeys(args))
    main(args)


def test_accounting_command():
    main(["accounting"])


def test_voice_chat(mocker):
    # We allow two calls in order to let the function be tested first and then terminate
    # the chat
    def _mock_listen(*args, **kwargs):  # noqa: ARG001
        try:
            _mock_listen.execution_counter += 1
        except AttributeError:
            _mock_listen.execution_counter = 0
        if _mock_listen.execution_counter > 1:
            raise KeyboardInterrupt
        return "foobar"

    mocker.patch("pyrobbot.voice_chat.VoiceChat.listen", _mock_listen)
    main(["voice", "--tts", "google"])
