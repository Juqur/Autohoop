## Basketball Hoop Project
### Overview
Welcome to the *documentation* for the Basketball Hoop project! Please note that this project was a result of a rush to completion before the start of a semester, so the documentation is lacking and the code quality may not be desirable. The project aimed to create a dynamic basketball hoop that could move both vertically and horizontally, ensuring that any ball thrown at it would, in *theory*, never miss.

### Project Description
The basketball hoop was primarily constructed using 3D printed parts, with additional support from scrap wood and stainless steel rods. Super glue and screws were used for assembly. The project utilized an Arduino Uno to control stepper motors via three TB6560 stepper motor driver controllers. Two controllers were employed for one axis due to uneven weight distribution. Two stepper motors were used for the Y-axis to counter gravity, and one for the X-axis. Additionally, three micro switches were integrated to detect when the moving parts reached the end of their respective axes.

### Challenges Faced
#### 1. Scale Limitations:
Issue: The project's small scale (approximately 35 by 30 cm grid) required precise and fast calculations.
Impact: This limitation demanded high accuracy, making the calculations more challenging.
#### 2. Ball Detection:
Issue: Fluctuations in the x and y positions due to camera inconsistencies affected the calculated trajectory significantly.
Impact: Despite accurate sensor readings, small-scale fluctuations resulted in imprecise ball positioning.
### Lessons Learned
#### Adhesive Challenges:
Hot glue proved ineffective on wood and PLA.
#### Soldering Skills:
Difficulties in soldering led to cold soldered connections.
#### Stepper Motor Belts:
Belts for stepper motors must be extremely tight to prevent skipping gears.
#### Motor Controller Adjustments:
Adjustable stepper motor controllers pull the exact amount specified, emphasizing the need for accurate power calculations to avoid damage.
Stepper Motor Libraries:
A dedicated stepper motor library was unnecessary for this project.
### Project Images (Sorry for bad lighting and blurry pictures)
#### Full project
![image](https://github.com/Juqur/Autohoop/assets/134002495/cf306e9b-d0be-4847-9a18-7ab8ed2aa3de)
Caption: The entire project, with the Kinect sensor placed atop the TV to capture ball movement.

#### Electronics
![image](https://github.com/Juqur/Autohoop/assets/134002495/267f1d23-542a-49bd-84f8-3ca0aca8e3a4)

Caption: Unprotected electronics, carefully arranged to avoid short circuits.

#### 3D Models
![image](https://github.com/Juqur/Autohoop/assets/134002495/e27f4f3d-62c1-49f4-bde1-71b097e53546)
![image](https://github.com/Juqur/Autohoop/assets/134002495/f0d29de6-9f7e-4c91-867c-a6aa36eabce9)
![image](https://github.com/Juqur/Autohoop/assets/134002495/6df131c2-a8e0-4917-b33a-72128af69f84)

Caption: Intricate 3D modeled pieces used in the project. My cats paw makes an appearance.

### Conclusion
While the project didn't achieve perfect accuracy due to scale limitations and ball detection challenges, it provided valuable lessons in practical electronics, 3D printing, and problem-solving. Feel free to explore the provided images to get a visual understanding of the project.
