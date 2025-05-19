# Use the official Freqtrade image
FROM freqtradeorg/freqtrade:stable

# Copy user_data into the container
COPY ft_userdata/user_data /freqtrade/user_data

# Set the working directory
WORKDIR /freqtrade

# Default command to run freqtrade
CMD ["freqtrade"]
