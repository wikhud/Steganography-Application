import numpy as np
from PIL import Image
import re
import math
import gui


class coder_class:
    
    def to_bin (self, data, n_bits):
        if isinstance (data, str):
            # encoding string, every single string character needs 8 bits
            return ''.join (format (ord (i), '08b') for i in data)
        elif isinstance (data, int) and n_bits == 8:
            # encoding integer in 8 bits
            return format (data, '08b')
        elif isinstance (data, int) and n_bits == 16:
            # encoding integer in 16 bits, even if only 8 are needed
            return format (data, '016b')
        elif isinstance (data, int) and n_bits == 24:
            # encoding integer in 24 bits, even if only 8 are needed
            return format (data, '024b')
        
    def combination (self, img_file):
        img_file = img_file.rotate (180)
        return img_file

    def encoder (self, input_img_file, secret_data, output_img_file, type):
        bits_to_hide = ''

        input_img = Image.open (input_img_file)      # loading input image
        input_img = self.combination (input_img)     # combination method hardens encryption (i.e. by image rotation)

        input_img = input_img.convert ('RGB')
        n_pixel_components = 3      # 3 components (because of RGB image type)
        width, height = input_img.size
        n_pixels = width * height

        img_array = np.array (list (input_img.getdata ()))     # array representation of input image

        # specyfing number of bytes of the largest secret possible to encode
        n_input_img_bytes = n_pixels * n_pixel_components
        max_n_usable_bytes = n_input_img_bytes / 8    # reason of /8 is that there's only 1 bit (last) from 1 byte of input image that could be used, so it needs 8 bytes of input image to encode 1 byte (8 bits) of secret

        # encoding starts with a header in the following format: letter specyfing type of the secret (text 'T' or image 'I'), number of bytes of secret and in the case of secret as image - its width  

        # in oreder to be represented in binary format, every single string character needs 8 bits, i.e. 1 byte
        # (which is why) to encode letter signifying type of secret  - it's 1 byte needed (1 [char])

	# asssumptions:
	# for secret as text max supported number of characters is 65535 (number of bytes needed to encode it is 2 (2 bytes i.e. 16 bits:     2 ^ 16 = 65535 [int]))
	# for secret as image max supported number of pixels is 5592405 (number of bytes to encode it is 3 (3 bytes i.e. 24 bits:     2 ^ 24 / 3 = 5592405 [pixels]))  
	# for secret as image its max supported width is 65535 (number of bytes to encode it is 2 (2 bytes i.e. 16 bits: 2 ^ 16 = 65535 [int])) 

        # for encoder and decoder, to be compatible with each other, need to share the same format
        # according to assumptions, the format is as follows: secret type - 1 byte; secret size (depending on its type) 'T' - 2 bytes, 'I' - 3 bytes; secret as image width - 2 bytes

        if type == 'T':
            n_header_bytes = 1 + 2      # specyfing header length (based on assumptions)
            
            n_secret_data_bytes = len (secret_data)      # specyfing secret as text size (i.e. number of characters i.e. bytes)
            
            # binary representation of data
            secret_as_text = self.to_bin ('T', 'str')
            bin_n_secret_data_bytes = self.to_bin (n_secret_data_bytes, 16)
            bits_to_hide = self.to_bin (secret_data, 'str')

            if (n_secret_data_bytes > 2 ** 16):       # veryfing if secret as text fits in allocated space (i.e. 2 bytes)
                gui.gui_class.warning (self, 'secret_too_long')
                return 1

            elif (n_header_bytes + n_secret_data_bytes > max_n_usable_bytes):    # veryfing if secret as text and header fit in input image
                gui.gui_class.warning (self, 'larger_input_size')
                return 1

            else:
                # indexes are used to iterate over subsequent elements of strings
                index1 = 0
                index2 = 0
                index3 = 0
                # bytes of secret (n-bytes) fits into         math.ceil (n-bytes * 8 / 3)        pixels
                for p in range (n_pixels):
                    for q in range (n_pixel_components):
                        # first part of the header needs 1 byte     ->      so: math.ceil (1 * 8 / 3) = math.ceil (2.7) = 3       ->      so: first part of the header will be encrypted in 3 pixels 
                        if p <= 2:   # the reason of 2 is that array elements in python count from 0 (i.e.: 0, 1, 2)
                            if index1 < len (secret_as_text):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + secret_as_text [index1], 2)
                                index1 += 1

                        # second part of the header needs 2 bytes     ->    so: math.ceil (2 * 8 / 3) = math.ceil (5.4) = 6  ->    so: second part of the header will be encrypted in 6 pixels 
                        elif 2 < p <= 8:    # the reason of 8 is that these are subsequent 6 bits (i.e.: 2 + 6 = 8)
                            if index2 < len (bin_n_secret_data_bytes):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + bin_n_secret_data_bytes [index2], 2)
                                index2 += 1
                            
                        elif 8 < p: # subsequent bits include: secret and then not replaced, unused bits
                            if index3 < len (bits_to_hide):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + bits_to_hide [index3], 2)
                                index3 += 1

                img_array = img_array.reshape (height, width, n_pixel_components)      # array is reshaped to original input image size
                output_img = Image.fromarray (img_array.astype ('uint8'), input_img.mode)     # image format representation of secret as image (first parameter defines color depth (uint8 means range 0 - 255))
                output_img = self.combination (output_img)   #tu cos
                output_img.save (output_img_file)

        if type == 'I':
            secret_bit_string = ''

            n_header_bytes = 1 + 3 + 2      # specyfing header based on set conditions

            secret_img = Image.open (secret_data)        # loading secret as image
            secret_img = secret_img.convert ('RGB')
            secret_width, secret_height = secret_img.size
            n_pixels_secret_img = secret_width * secret_height
            
            secret_img_array = np.array (list (secret_img.getdata ()))      # array representation of secret as image

            n_secret_data_bytes = n_pixels_secret_img * n_pixel_components       # specyfing secret as image size (i.e. number bytes (to encode image pixels))

            # binary representation of data
            secret_as_img = self.to_bin ('I', 'str')
            bin_n_secret_data_bytes = self.to_bin (n_secret_data_bytes, 24)
            bin_secret_width = self.to_bin (secret_width, 16)
            
            # one-dimensional array representation of secret as image (elements of array are pixel components values)
            for p in range (n_pixels_secret_img):
                for q in range (n_pixel_components):
                    secret_bit_string += str (secret_img_array [p] [q]) + ' '
            secret_bit_string = secret_bit_string.split ()
            
            # convertion of created array values into binary format
            for i in range (len (secret_bit_string)):
                secret_bit_string [i] = self.to_bin (int (secret_bit_string [i], 10), 8)

            # binary representation of secret as image (string of image bits)
            for i in range (len (secret_bit_string)):
                bits_to_hide += secret_bit_string [i]
                
            if (n_secret_data_bytes > 2 ** 24):       # veryfing if secret as image fits in alocated space (i.e. 3 bytes)
                gui.gui_class.warning (self, 'secret_too_large')
                return 1

            elif (secret_width > 2 ** 16):        # veryfing if secret as image width fits in alocated for it space i.e. 2 bytes
                gui.gui_class.warning (self, 'secret_image_width')
                return 1

            elif (n_header_bytes + n_secret_data_bytes > max_n_usable_bytes):        # veryfing if secret as image and header fit in input image
                gui.gui_class.warning (self, 'larger_input_size')
                return 1

            else:
                # everything below -> same thing (calculations, rules etc.) as for secret as text
                index1 = 0
                index2 = 0
                index3 = 0
                index4 = 0
                for p in range (n_pixels):
                    for q in range (n_pixel_components):
                        if p <= 2:
                            if index1 < len (secret_as_img):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + secret_as_img [index1], 2)
                                index1 += 1

                        elif 2 < p <= 10:
                            if index2 < len (str (bin_n_secret_data_bytes)):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + bin_n_secret_data_bytes [index2], 2)
                                index2 += 1

                        elif 10 < p <= 16:
                            if index3 < len (bin_secret_width):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + bin_secret_width [index3], 2)
                                index3 += 1

                        elif 16 < p:
                            if index4 < len (bits_to_hide):
                                img_array [p] [q] = int (bin (img_array [p] [q]) [:-1] + bits_to_hide [index4], 2)
                                index4 += 1
                
                img_array = img_array.reshape (height, width, n_pixel_components)
                #tego zapisu nie rozumiem
                output_img = Image.fromarray (img_array.astype ('uint8'), input_img.mode)
                output_img = self.combination (output_img)
                output_img.save (output_img_file)

    def decoder (self, input_img_path):
        bin_n_secret_data_bytes = ''
        n_secret_data_bytes = ''
        hidden_bits = ''
        secret_data = ''
        bin_secret_kind = ''
        secret_kind = ''

        input_img = Image.open (input_img_path)     # loading input image
        input_img = self.combination (input_img)    #tutaj cos

        input_img = input_img.convert ('RGB')
        n_pixel_components = 3      # 3 components because of RGB image type
        width, height = input_img.size
        n_pixels = width * height

        img_array = np.array (list (input_img.getdata ()))      # array representation of input image

        # secret encryption starts with a header containing information such as: letter specyfing type of the secret (text 'T' or image 'I'), number of bytes of secret and in the case of an secret as image - its width  
        
        # to be represented in binary format every single string character needs 8 bits, i.e. 1 byte
        # (this is why) to encode letter signifying type of secret  - it's 1 byte needed (1 [char])
        # assuming the number of secret as text' characters (bytes) wouldn't be grater than 65535, number of bytes needed to encode it is 2 (2 bytes i.e. 16 bits:     2 ^ 16 = 65535 [int])
        # assuming the number of secret as image' pixels wouldn't be grater than 5592405, number of bytes to encode it is 3 (3 bytes i.e. 24 bits:     2 ^ 24 / 3 = 5592405 [pixels])
        # assuming secret as image' width wouldn't be grater than 65535, number of bytes to encode it is 2 (2 bytes i.e. 16 bits: 2 ^ 16 = 65535 [int])

        # for encoder and decoder to be compatible with each other, values of every part of header have to be the same, so it's determined erlier (above)
        # in this case values are assigned like: secret's type - 1 byte; secret's 'lenght' (depending on its type) 'T' - 2 bytes, 'I' - 3 bytes; secret as image's width - 2 bytes

        # n-bytes fits into         math.ceil (n-bytes * 8 / 3)        pixels
        for p in range (n_pixels):
            for q in range (n_pixel_components):
                # first part of the header needs 1 byte     ->      so: math.ceil (1 * 8 / 3) = math.ceil (2.7) = 3       ->      so: first part of the header will be encrypted in 3 pixels 
                if p <= 2:      # the reason of 2 is that array elements in python count from 0 (i.e.: 0, 1, 2)
                    bin_secret_kind += bin (img_array [p] [q]) [-1]

        # there are often unused bits left because of ceiling function
        # each pixel has 3 bytes itself, because it contains 3 pixel components, each one byte 
        # information is encoded only in the last bit of each component, so I need 8 bytes to encode my 8-bit information 
        # for example, first part of the header is encoded in 1 byte, i.e. 8 bits
        # 8 bytes fit into 3 pixels (3 pixels *each * 3 bytes = 9  ->  3 * 3 = 9) and because of the ceiling, there's redundant 1 byte which means redundant 1 bit for information 
        # information will be read correctly when the last redundant bit is removed:
        bin_secret_kind = bin_secret_kind [:-1]

        secret_kind = chr (int (bin_secret_kind, 2))

        if secret_kind == 'T':
            for p in range (n_pixels):
                for q in range (n_pixel_components):
                    # second part of the header needs 2 bytes     ->    so: math.ceil (2 * 8 / 3) = math.ceil (5.4) = 6  ->    so: second part of the header will be encrypted in 6 pixels 
                    if 2 < p <= 8:  # the reason of 8 is that these are another / subsequent 6 bits (i.e.: 2 + 6 = 8)
                        bin_n_secret_data_bytes +=  bin (img_array [p] [q]) [-1]
                    elif 8 < p:     # another / subsequent bits include firstly secret and then not replaced / unused bits
                        hidden_bits +=  bin (img_array [p] [q]) [-1]

            # same thing (calculations, rules etc.) as for the bin_secret_kind variable (only for 16 bits) or in brief:
            # 16 characters (2 bytes) were encoded in 6 pixels (each 3 colors [components]), i.e. 16 / 3    ->      6 pixels including 2 redumdant bits from 2 colors [components]
            bin_n_secret_data_bytes = bin_n_secret_data_bytes [:-2]
            
            n_secret_data_bytes = int (bin_n_secret_data_bytes, 2)      # decimal representation of n_secret_data_bytes

            # hidden bits are splited in 8 so later it could be treated as bytes (8 bites) and then converted to human-readable format
            hidden_bits = re.findall ('........', hidden_bits)
            for i in range (n_secret_data_bytes):
                secret_data += chr (int (hidden_bits [i], 2))

            message = ('Decryption successfull! Hidden message:')

            stuff_to_return = [secret_kind, secret_data, message]
            return stuff_to_return
            
        elif secret_kind == 'I':
            bin_secret_width = ''

            for p in range (n_pixels):
                for q in range (n_pixel_components):
                    if 2 < p <= 10:     # same thing (calculations, rules etc.) as for secret as text
                        bin_n_secret_data_bytes += bin (img_array [p] [q]) [-1]
                    elif 10 < p <= 16:      # third part of the header needs 3 bytes     ->    so: math.ceil (3 * 8 / 3) = math.ceil (8) = 8  ->    so: third part of the header will be encrypted in 8 pixels (and there are not redundant bits!)
                        bin_secret_width += bin (img_array [p] [q]) [-1]
                    elif 16 < p:    # same thing (calculations, rules etc.) as above
                        hidden_bits += bin (img_array [p] [q]) [-1]

            bin_secret_width = bin_secret_width [:-2]   # same thing (calculations, rules etc.) as for secret as text

            # decimal representation of data
            n_secret_data_bytes = int (bin_n_secret_data_bytes, 2)
            secret_width = int (bin_secret_width, 2)

            # calculating secret as image height (width already known)
            n_pixels_secret_img = math.floor (n_secret_data_bytes / n_pixel_components)
            secret_height = int (n_pixels_secret_img / secret_width)

            hidden_bits = re.findall ('........', hidden_bits)		# hidden bits are splited in 8, so it could be treated as bytes (8 bites)
            for i in range (n_secret_data_bytes):			# creation of string of hidden bits again, but this time a shorter one with a length corresponding to the length of the secret
                secret_data += hidden_bits [i]
            secret_data = re.findall ('........', secret_data)		# split of string in 8 again, so it could be treated as bytes (8 bites)
            for i in range (len (secret_data)):				# creation of string of numbers that are consecutive values of pixel components of secret as image (in decimal form)
                secret_data [i] = str (int (secret_data [i], 2))

            # array is created out of secret_data string and then reshaped to original secret as image size
            secret_img_array = np.array (secret_data)
            secret_img_array = secret_img_array.reshape (secret_height, secret_width, n_pixel_components)

            output_img = Image.fromarray (secret_img_array.astype ('uint8'))    # image format representation of secret as image 

            message = ('Decryption successfull! Hidden message:')

            stuff_to_return = [secret_kind, output_img, message]
            return stuff_to_return
        else:
            message = ('Decryption failure! No hidden message found.')
            stuff_to_return = [message]
            return stuff_to_return
