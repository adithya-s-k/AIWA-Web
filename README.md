# AIWA - AI assisted Workout Assistant 

Especially during Covid and lockdown, keeping fit has become a problem. This is where Fiton comes in, it uses visual processing technologies and A.I to guide you through different exercises in a fun way.
Fiton also makes sure you are performing the exercises in an optimal way, preventing injury.
It comes with many additional features such as posture detection and a blink counter to reduce eye strain.
It also has yoga posture detection to correct your yoga posture and we have also given you the ability to train the model with your own yoga exercises.
It also comes with a game with motion tracking to make your workout a fun experience.

Challenges We ran into
-Problems in training the A.I model.
-The code was inefficient and the visual processing was laggy due to less computing power.
-Figuring out and calibrating the correct workout methods(angles your body forms during exercises, etc) was challenging and made it difficult to decide the correct workout method and procedure.
-Not enough resources to make a web-based tool, so it was restricted to an application on the local PC.
-figuring out the mathematical constraints and equations for the exercises posed challenging(min-max angle, distances, etc)

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

We are using a [face_recognition](https://face-recognition.readthedocs.io/en/latest/readme.html) library to detect faces and compare faces.

The teacher will have to take a photo of the class and upload it to the website at the beginning of the class.She should take the photo in such a 
way that everyones face is properly visible.
We now will use facial detection to detect the faces and put a box around them as shown below.
![.](https://ibb.co/SXpN4yz)
After the teacher verifies that everyone's face is visible she will upload the photos on the website.
In the backend each isolated face is stored and compared with a pre-existing data base of student faces.
Here we will be using the face comparison feature and we will be giving attendance to all the students whose faces match.
We will show the absentees list to the teacher where she can call out and verify.

After the face matches the matched face will be added to the database for future comparison and thus the accuracy of the model will keep on increasing.

Here is the [flow chart](https://www.figma.com/file/ssy2MQrWiOkHtrcbPdV7mg/Attendace-Tracking-workflow?node-id=0%3A1)

Here is the [Project Video](https://youtu.be/mRgZdZOKjTk)




## Advantage over existing solutions.

- Quicker and Faster.
- Less error prone.
- No need for external hardware like a camera display.
- The student will have to be physically present in the class in order to get attendance. Faking attendance will become difficult.
- The accuracy increases day by day.


## Tech Stack

**Client:** HTML ,CSS ,Bootstrap

**Server:** Flask(Python)


## Authors

- [@adithya-s-k](https://github.com/adithya-s-k)
- [@senju-hashirama](https://github.com/senju-hashirama)
- [@aaryanhb](https://github.com/aaryanhb)


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)]()
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adithya-s-kolavi-127a561a8/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/adithya_s_k)


## Contributing

Contributions are always welcome!

You can fork the repository and create a pullrequest for contributing.

Please adhere to this project's `code of conduct`.