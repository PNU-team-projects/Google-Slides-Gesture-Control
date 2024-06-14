# Gesture control for Google Slides

## Setting up a project

#### 1) Clone the repository
```
git clone https://github.com/PNU-team-projects/Google-Slides-Gesture-Control.git 
cd Google-Slides-Gesture-Control
```

#### 2) Create an environment and install requirements

```
py -m venv env
env\Scripts\activate

pip install -r requirements.txt
```

#### 3) Download model architecture and weights form Colab Notebook
[![Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mthUmFjGTuqB5rgLFHg8rU8Jy8fk-fDP?usp=sharing)

#### 4) Run the application
```
py app.py --url "your url"
```

| Argument     | Desctiption               | 
| ------------ | ------------------------- |  
| `--url`      | link to the presentation  |
| `--width`    | camera output width       |   
| `--height`   | camera output height      |


## Functions
| Action                                     | Gesture               | 
| ------------------------------------------ | ------------------------- |  
| Enter/Leave full screen mode               | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/bf27987f-3cfa-498d-a04b-4fa8e8658dc4) |
| Start presentation from the first slide    | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/29e8df5c-d476-4f0a-8201-b309baa91b94) |   
| Next slide                                 | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/22f70159-cc8e-4ec1-a991-ac4f3c1f6c50) |
| Prev slide                                 | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/496a478c-0063-4125-9f6a-ad3d58ed155a) |
| End the presentation                       | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/8a926829-6647-49d2-86b4-b5c3b949007b) |
| Move slide up                              | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/9dab5638-2d5a-42fb-841e-a402be26478d) |
| Move slide down                            | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/8dd25955-0c4d-49c0-b035-437adc516e8c) |
| Close the application                      | ![image](https://github.com/PNU-team-projects/Google-Slides-Gesture-Control/assets/125756054/78d846ce-3891-4b29-b335-0f3628351e9b) |
