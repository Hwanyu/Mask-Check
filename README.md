# Mask-Check
마스크 검출 코드

1. binarize the picture
2. Do Threshold
3. Detect white parts using roi
4. Put a blue dot on the part found using roi
5. Find blue dot points connected in 8 directions using Connected Components
6. print only the largest part
