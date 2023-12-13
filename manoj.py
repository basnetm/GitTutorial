from PIL import Image

# Function to encode a message into an image
def encode_image(source_img_path, secret_msg, output_img_path):
    # Open the source image
    img = Image.open("C:\Users\Acer\OneDrive\Pictures\Screenshots")

    # Convert the message to binary
    binary_msg = ''.join(format(ord(char), '08b') for char in secret_msg)

    # Check if the message is too large to fit in the image
    if len(binary_msg) > img.width * img.height * 3:
        raise Exception("Message is too large to hide in the image")

    data_index = 0
    encoded_pixels = list(img.getdata())

    for i, pixel in enumerate(encoded_pixels):
        # Convert pixel values to binary
        pixel = list(pixel)
        for color_channel in range(3):
            if data_index < len(binary_msg):
                # Replace the least significant bit with the message bit
                pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_msg[data_index])
                data_index += 1
            else:
                break

        # Update the pixel data
        encoded_pixels[i] = tuple(pixel)

    # Create a new image with the encoded data
    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(encoded_pixels)

    # Save the encoded image
    encoded_img.save(output_img_path)

# Function to decode a message from an image
def decode_image(encoded_img_path):
    # Open the encoded image
    encoded_img = Image.open(encoded_img_path)

    binary_msg = ""
    for pixel in encoded_img.getdata():
        for color_channel in pixel:
            binary_msg += str(color_channel & 1)

    # Convert binary message to text
    message = ""
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i + 8]
        message += chr(int(byte, 2))

    return message

# Main program
if __name__ == "__main__":
    source_image_path = "C:\Users\Acer\OneDrive\Pictures\Screenshots"
    secret_message = "Hello, this is a secret message!"

    # Encode the secret message into the image
    encoded_image_path = "encoded_image.png"
    encode_image(source_image_path, secret_message, encoded_image_path)

    # Decode the secret message from the encoded image
    decoded_message = decode_image(encoded_image_path)
    print("Decoded Message:", decoded_message)
