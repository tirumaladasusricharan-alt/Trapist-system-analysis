# Trapist-system-analysis
🌌TRAPPIST-1 SIGNAL ISOLATION OR PLANETARY SYSTEM ANALYSIS

In multi-planetary systems, the biggest headache isn't just finding a planet -it's dealing with "signal competition." While digging through NASA's TESS data, I built a custom pipeline to tease out the fainter transit signatures in the TRAPPIST-1 system. Basically, I wanted to bridge that tricky gap between "I think I see something" and actually confirming a real candidate.

📡TRAPPIST-1b is a Signal Hog

The heavy hitter here is TRAPPIST-1b. Its transit creates such a massive dip in the light curve that it effectively drowns out everything nearby. To get around this, I used a method called "Iterative Signal Subtraction".

Essentially, I had to mathematically "blind" the data to the primary planet's orbital period. By masking that dominant flux, I could scrub the data clean enough to hunt for the much weaker signals of "Planet 1c". It's a mandatory step-if you don't strip away that primary "noise," the secondary planets stay buried in the math.

🌐TRAPPIST-1c (The "Venus Twin")

Isolating TRAPPIST-1c was the real test. It's often called a "Venus Twin" because of its size, but recent JWST data suggests it might actually be a bare rock with almost no atmosphere. My pipeline focuses on boosting the Signal-to-Noise Ratio (SNR) for le to help tell the difference between its 2.42-day signature and random stellar noise, like starspots.

📔LIBRARIES USED:

The "engine" under the hood is a Python-based stack:

"NumPy": For the heavy-duty signal processing.

"Lightkurve": For managing the astronomical time-series data.

"Streamlit": I wrapped everything into a dashboard so I could tweak parameters in real-time.

"Matplotlib":For rendering the phase-folded light curves.

🌍CONCLUSION OR THE BIGGER PICTURE:
This kind of work is the "ground-floor" for what agencies like "NASA (USA)","ESA (Europe)", "JAXA (Japan)", and "ISRO (India)" are doing right now. Whether it's the James Webb Space Telescope looking for atmospheres or upcoming missions like PLATO, the goal is the same: uncovering the subtle complexities of a system by systematically removing the most obvious features.
