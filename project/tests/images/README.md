# Image fixture provenance

All four images are synthetic fixtures rendered by `project/tools/make_image_fixtures.py`
on 20 October 2026. They contain no real people, employers, names or applicant data.
They are not claimed to be real phone photos.

- `clean.jpg`: readable junior frontend role and three requirements.
- `degraded.jpg`: role title obscured; downscaled/compressed/blurred text.
- `ambiguous.jpg`: Junior / Senior role, requiring human confirmation.
- `not-applicable.jpg`: unrelated shopping list.

Each is below 2 MB. The API downsizes the longest edge to <=1024 px before sending.
