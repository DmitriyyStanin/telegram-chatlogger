# Use the official PHP image as the base image
FROM php:7.4-apache

# Copy the application files into the container
COPY . /var/www/html

# Set the working directory in the container
WORKDIR /var/www/html

# Install necessary PHP extensions
RUN apt update && apt install git
git clone https://github.com/kibersportovich/telegram-chatlogger
cd telegram-chatlogger
pip3 install -r requirements.txt

# Expose port 80
EXPOSE 80

# Define the entry point for the container
CMD ["apache2-foreground"]
