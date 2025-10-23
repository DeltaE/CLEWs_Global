FROM ubuntu:24.04
LABEL authors="junoh"

RUN apt update -y && apt upgrade -y && apt install -y \
      python3 python3-pip \
      glpk-utils coinor-cbc \
	  wget curl \
      git \
      zsh;

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN mkdir ~/working
# Default powerline10k theme, no plugins installed
RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh&& \
	/bin/bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
	rm ~/miniconda3/miniconda.sh && \
	. ~/miniconda3/bin/activate && \
    conda init --all
CMD ["zsh"]

