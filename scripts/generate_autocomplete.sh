#!/usr/bin/env zsh
# TODO: Add the following to the "init"
# try:
#     import click_completion2
#     click_completion.init()
# except Exception as e:
#     logger.debug("click_completion not installed")
# Generate BASH autocomplete
export SHELL=/usr/bin/bash
bash -c "echo $SHELL && _RAPHIDOC_COMPLETE=source raphidoc > raphidoc-complete-bash.sh"

# Generate ZSH autocomplete
export SHELL=/usr/bin/zsh
zsh -c "_RAPHIDOC_COMPLETE=source raphidoc > raphidoc-complete-zsh.sh"
