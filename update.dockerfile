FROM continuumio/anaconda3:latest

ENV TZ='Asia/Tokyo'
RUN pip install yfinance mplfinance pandas_datareader

WORKDIR /root
CMD /root/go.update.sh
