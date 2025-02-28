final score calculation 
INSERT INTO ReportCards (student_id, academic_score, physical_score, emotional_social_score, life_skills_score, creativity_score, sports_score, overall_score, remarks, date_of_creation)
SELECT 
    s.student_id,
    COALESCE(AVG(g.marks_obtained), 0) AS academic_score,
    COALESCE(AVG(pg.fitness_score + pg.stamina_level + pg.flexibility_score) / 3, 0) AS physical_score,
    COALESCE(AVG(esg.emotional_intelligence_score + esg.confidence_score + esg.teamwork_score + esg.leadership_score) / 4, 0) AS emotional_social_score,
    COALESCE(AVG(lsg.time_management_score + lsg.adaptability_score + lsg.resilience_score + lsg.problem_solving_score) / 4, 0) AS life_skills_score,
    COALESCE(AVG(ce.art_music_score + ce.volunteering_hours) / 2, 0) AS creativity_score,
    COALESCE(AVG(ssp.performance_score), 0) AS sports_score,
    (
        (COALESCE(AVG(g.marks_obtained), 0) * 0.4) +
        (COALESCE(AVG(pg.fitness_score + pg.stamina_level + pg.flexibility_score) / 3, 0) * 0.15) +
        (COALESCE(AVG(esg.emotional_intelligence_score + esg.confidence_score + esg.teamwork_score + esg.leadership_score) / 4, 0) * 0.15) +
        (COALESCE(AVG(lsg.time_management_score + lsg.adaptability_score + lsg.resilience_score + lsg.problem_solving_score) / 4, 0) * 0.1) +
        (COALESCE(AVG(ce.art_music_score + ce.volunteering_hours) / 2, 0) * 0.1) +
        (COALESCE(AVG(ssp.performance_score), 0) * 0.1)
    ) AS overall_score,
    CASE 
        WHEN overall_score >= 90 THEN 'Excellent Performance'
        WHEN overall_score >= 75 THEN 'Good Performance'
        ELSE 'Needs Improvement'
    END AS remarks,
    CURDATE() AS date_of_creation
FROM Students s
LEFT JOIN Grades g ON s.student_id = g.student_id
LEFT JOIN PhysicalGrowth pg ON s.student_id = pg.student_id
LEFT JOIN EmotionalSocialGrowth esg ON s.student_id = esg.student_id
LEFT JOIN LifeSkillsGrowth lsg ON s.student_id = lsg.student_id
LEFT JOIN CreativityExtracurriculars ce ON s.student_id = ce.student_id
LEFT JOIN StudentSportsParticipation ssp ON s.student_id = ssp.student_id
GROUP BY s.student_id;


-- Parents Table
CREATE TABLE Parents (
    parent_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Class Table
CREATE TABLE Classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_name VARCHAR(20) NOT NULL,
    start_year INT NOT NULL,
    end_year INT NOT NULL,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- Teachers Table
CREATE TABLE Teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Admin Table
CREATE TABLE Admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- Announcements Table
CREATE TABLE Announcements (
    announcement_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    date_created DATE NOT NULL,
    admin_id INT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id)
);

-- Students Table
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    parent_id INT NOT NULL,
    class_id INT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES Parents(parent_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);

-- Subjects Table
CREATE TABLE Subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100) NOT NULL,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- Grades Table (Academic Performance)
CREATE TABLE Grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    marks_obtained DECIMAL(5,2) NOT NULL,
    subject_id INT NOT NULL,
    student_id INT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Physical Growth Table
CREATE TABLE PhysicalGrowth (
    physical_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    fitness_score DECIMAL(5,2) NOT NULL,
    stamina_level DECIMAL(5,2) NOT NULL,
    flexibility_score DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Emotional & Social Growth Table
CREATE TABLE EmotionalSocialGrowth (
    emotional_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    emotional_intelligence_score DECIMAL(5,2) NOT NULL,
    confidence_score DECIMAL(5,2) NOT NULL,
    teamwork_score DECIMAL(5,2) NOT NULL,
    leadership_score DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Life Skills Growth Table
CREATE TABLE LifeSkillsGrowth (
    life_skill_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    time_management_score DECIMAL(5,2) NOT NULL,
    adaptability_score DECIMAL(5,2) NOT NULL,
    resilience_score DECIMAL(5,2) NOT NULL,
    problem_solving_score DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Creativity & Extracurricular Activities Table
CREATE TABLE CreativityExtracurriculars (
    creativity_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    art_music_score DECIMAL(5,2) NOT NULL,
    volunteering_hours INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Sports Participation Table
CREATE TABLE StudentSportsParticipation (
    sport_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    sport_name VARCHAR(50) NOT NULL,
    performance_score DECIMAL(5,2) NOT NULL,
    level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Multi-Dimensional Report Card Table
CREATE TABLE ReportCards (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    academic_score DECIMAL(5,2) NOT NULL,
    physical_score DECIMAL(5,2) NOT NULL,
    emotional_social_score DECIMAL(5,2) NOT NULL,
    life_skills_score DECIMAL(5,2) NOT NULL,
    creativity_score DECIMAL(5,2) NOT NULL,
    sports_score DECIMAL(5,2) NOT NULL,
    overall_score DECIMAL(5,2) NOT NULL,
    remarks TEXT NOT NULL,
    date_of_creation DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);


-- Academic Score Scale
CREATE TABLE AcademicScoreScale (
    scale_id INT PRIMARY KEY AUTO_INCREMENT,
    min_score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    grade VARCHAR(10) NOT NULL,
    remarks VARCHAR(255) NOT NULL
);

-- Physical Score Scale
CREATE TABLE PhysicalScoreScale (
    scale_id INT PRIMARY KEY AUTO_INCREMENT,
    min_score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    remarks VARCHAR(255) NOT NULL
);

-- Emotional & Social Score Scale
CREATE TABLE EmotionalSocialScoreScale (
    scale_id INT PRIMARY KEY AUTO_INCREMENT,
    min_score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    remarks VARCHAR(255) NOT NULL
);

-- Life Skills Score Scale
CREATE TABLE LifeSkillsScoreScale (
    scale_id INT PRIMARY KEY AUTO_INCREMENT,
    min_score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    remarks VARCHAR(255) NOT NULL
);

-- Creativity & Extracurricular Score Scale
CREATE TABLE CreativityScoreScale (
    scale_id INT PRIMARY KEY AUTO_INCREMENT,
    min_score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    remarks VARCHAR(255) NOT NULL
);

-- Sports Score Scale
CREATE TABLE SportsScoreScale (
    scale_id INT PRIMARY KEY AUTO_INCREMENT,
    min_score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    remarks VARCHAR(255) NOT NULL
);
