# AIWA - AI assisted Workout Assistant 

### Introduction of the idea:

Especially during Covid and lockdown, keeping fit has become a
problem. This is where AIWA comes in, it uses visual processing
technologies and A.I to guide you through different exercises in a
fun way. AIWA also makes sure you are performing the exercises in
an optimal way, preventing injury. It comes with many additional
features such as posture detection and a blink counter to reduce
eye strain. It also comes with a game with motion tracking to make
your workout a fun experience.

### Problem statement :

Maintaining good physical and mental health during lockdown has
been a very challenging thing for many people as they wont be
able to visit the gym or yoga classes so often and also their social
interaction with other people has decreased.

### Purpose:

Especially during Covid and lockdown, keeping fit has become a problem.
This is where AIWA comes in, it uses visual processing technologies and
A.I to guide you through different exercises in a fun way
lack of accessibility: a large portion of the common populace does not
have access to gyms or gym trainers and therefore prefer to workout and
get some exercise on their own. This means they are more prone to
injuries, may lose motivation and not reach their end goal. During these
trying times of the covid 19 pandemic, this problem is further
highlighted.
day-to-day applicability: Things like bad posture and eye strain, although
seemingly trivial, may have complicated long-term effects. People
knowingly or unknowingly overlook these things. This is where AIWA
comes in.

### Scope:
We all can agree due to lockdown our physical state has
degraded due to lack of exercise and metal health has become
worse . This is were AIWA comes in it will help you in keeping fit
and tracks your emotional state throughout the day so that you
can improve your physical and mental health.

### Methodology:
We will be using image processing paired with a trained ML/DL
module to count the number of repetitions of an exercise you
are doing and tells if you are doing something wrong.
For Posture detection we will be calibration the model every
time as the user will be sitting in different place so that it is
more versatile.

We built this project for NMIT Hackthon 22
## Installation

Download the zip file or clone the repository

```bash
git clone https://github.com/adithya-s-k/AIWA-Web.git
```
Go to the repository where you have cloned and run app.py
```bash
python app.py
```

    
## How it works
The project is built using Python and Flask.

We are using a [mediapipe](https://google.github.io/mediapipe/) and we are using the pose estimation model.
By using the pose estimation model ,we will be able to get the coordinates of 32 points on our body as shown below.
\
![Mediapipe coordinates](https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png)
\
Using these coordinates we can calculate the angle, distance between the points.
Thus we can set parameters for different exercises depending on the angle between the joints and calculate the number of reps a person is doing in each exercise as show below
\
We have also used a pre trained model from Keras.Using this we are able to detect different yoga poses a person is doing as shown below.
\
Preview of the website
\
![HomePage Preview](https://github.com/adithya-s-k/AIWA-Web/blob/master/static/Frame_home.png)
Here is the [Project Video](https://youtu.be/GDy-AMGFmwc) This video is of the offline version of this app

## Advantage over existing solutions.
- You can workout safely at the comfort of your house
- Current workout apps can show only show images and videos of exercise but AIWA will show you images and videos of exercises and also monitor them using your camera
- It is easier than going to the gym.
- you wont be able to get personal attention while attending yoga classes online.

## Future Implementations
- Adding a voice assitant to guide you during your workouts and also motivate you to do more.
- Training the yoga ML model with professinals
- Increasing the efficiency by trying out different pose estimation models
- 



## Tech Stack

**Client:** HTML ,CSS ,Bootstrap

**Server:** Flask(Python)


## Authors

- [@adithya-s-k](https://github.com/adithya-s-k)
- [@senju-hashirama](https://github.com/senju-hashirama)


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)]()
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adithya-s-kolavi-127a561a8/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/adithya_s_k)


## Contributing

Contributions are always welcome!

You can fork the repository and create a pullrequest for contributing.

Please adhere to this project's `code of conduct`.