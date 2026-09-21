# From a still image to a video · 从静态图到视频

[Creator examples](x-videos.md) · [Input guide](recipe-access.md)

This is an authored workflow, not a reproduced creator prompt or completed video test. GPT Image 2.5 supplies the still image; animation requires a separate video tool such as Seedance 2.5. The Flyne free image offer does not establish free video access. Check the selected video tool’s current availability, duration settings and price.

这是一套本库编写的操作模板，未完成视频实测，也不是 X 作者未公开的原提示词。先生成并确认静态图，再用单独的视频工具制作动画。图片免费入口不代表视频也免费。

## 1. Create and review a still

Start with [P092: bakery campaign](../prompts/16-flyne-x-discoveries.md#p092). Choose a supported aspect ratio and copy one language block. Inspect loaf count, hands, crust and lettering. Save a clean approved image before animating; do not use the X author’s image as your input without permission.

先用 P092 生成面包广告图，检查面包数量、手部、表皮与文字，再保存确认稿。不要把作者原帖配图当作本库生成结果。

## 2. Animate the approved image

Upload that one approved still into a video tool with image-to-video support. If a five-second duration is available, use the following independently authored motion brief. Otherwise adjust the duration in both the tool and prompt.

```text
Create a five-second shot from the supplied approved bakery image. Use a slow, subtle camera push-in. Preserve the number, shapes and positions of the loaves, the hands, clothing, lighting and all existing lettering. Keep the subject still; do not introduce a new person, prop, logo or text. No cuts, object morphing, hand movement or sudden camera motion. End with the same composition slightly closer.
```

```text
以附上的面包广告确认稿制作五秒镜头。镜头缓慢、轻微推进；保持面包数量、形状和位置，以及手部、服装、光线和已有文字。主体静止，不新增人物、道具、标志或文字。不切镜，不让物体变形，不增加手部动作，不突然运镜。结尾保持相同构图，仅略微拉近。
```

## 3. Review and record the actual result

Watch the entire clip, including the opening and final frames. Reject loaf duplication, changing fingers, warped text or flicker. Record the tool’s displayed model name, date, actual duration, aspect ratio, exact prompt, input image and output; do not infer an unavailable model version. Record failure as failure. Only label this workflow tested after saving and reviewing an actual result.

完整播放，检查首尾帧、面包数量、手指、文字和闪烁。记录页面显示的模型、日期、实际时长、比例、准确提示词、输入图和输出。失败也要保留记录；实际生成并检查视频之后才能标为已实测。
