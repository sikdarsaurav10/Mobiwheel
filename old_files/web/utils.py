import os
import string
import random
# from PIL import Image
from web import app, mail
from flask_mail import Message


def send_mail(user_info):
    msg = Message('New Repair Request',
                  recipients=['sikdarsaurav10@gmail.com'])
    if len(user_info) == 5:
        msg.body = "Phone Brand: " + user_info[0] + "\nPhone Model: "\
                    + user_info[1] + "\nName: " + user_info[2]\
                    + "\nProblem: " + user_info[3] +\
                    "\nContact Number: " + user_info[4]
    else:
        msg.body = "Phone Brand: " + user_info[0] + "\nPhone Model: "\
                    + user_info[1] + "\nName: " + user_info[2]\
                    + "\nContact Number: " + user_info[3]
    mail.send(msg)


def save_pic(phone_pic):
    alphabet = string.ascii_letters + string.digits
    random_hex = ''.join(random.choice(alphabet) for i in range(8))
    # random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(phone_pic.filename)
    file_ext_allowed = [".jpg", ".png", ".jpeg"]
    if f_ext in file_ext_allowed:
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path,
                                'static/images/phones/',
                                pic_fn)

        # output_size = (350, 450)
        # i = Image.open(phone_pic)
        # i.thumbnail(output_size)
        phone_pic.save(pic_path)

        return pic_fn
    return "Not allowed"


def save_title_pic(phone_pic):
    alphabet = string.ascii_letters + string.digits
    random_hex = ''.join(random.choice(alphabet) for i in range(8))
    # random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(phone_pic.filename)
    file_ext_allowed = [".jpg", ".png", ".jpeg"]
    if f_ext in file_ext_allowed:
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path,
                                'static/images/phones/titleImages',
                                pic_fn)

        # output_size = (180, 250)
        # i = Image.open(phone_pic)
        # i.thumbnail(output_size)
        phone_pic.save(pic_path)

        return pic_fn
    return "Not allowed"


def generate_phone_id(brand, model):
    _ = brand[:3] + '-' + model + '-'
    alphabet = string.ascii_letters + string.digits
    str1 = ''.join(random.choice(alphabet) for i in range(5))
    code = _+str1
    return code
