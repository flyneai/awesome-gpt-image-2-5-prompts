#!/usr/bin/env python3
"""Build the source-linked video index; never download third-party media."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build():
    records=json.loads((ROOT/'data/x-videos.json').read_text())['videos']
    lines=['# GPT Image 2.5: from still images to video · 从图片到视频','','[Flyne README](../README.md) · [Image prompts](../prompts/16-flyne-x-discoveries.md)','','These creator posts describe workflows that use GPT Image 2.5 for still images and a separate model for motion. Click a preview to watch on X. The video player and poster were observed on each original post; model roles are author statements, not independent backend verification. Full playback was not audited.','','这些案例先生成图片，再使用另一个模型制作视频。点击预览图打开作者原帖播放。已核对原帖文字、视频播放器和预览图，未逐帧审查完整视频。原帖未公开完整提示词，因此下列条目不计入提示词数量。','','Third-party previews and videos are linked remotely and are not included in the MIT license. No local video file is redistributed.','']
    lines += ['[Step-by-step image-to-video template / 图转视频操作模板](image-to-video-workflow.md) — authored workflow; video output not tested / 编写模板，尚未实测视频输出。', '']
    for v in records:
        lines += [f'## {v["id"]} · {v["title"]}','',f'[![{v["title"]} — watch original video]({v["poster_url"]})]({v["url"]})','',f'**[Watch on X / 在 X 播放]({v["url"]})** · {v["author"]} ({v["handle"]}) · {v["published"]}','',v['summary'],'',f'**Image:** {v["image_model"]} · **Video:** {v["video_model"]}','',f'**Prompt availability:** {v["prompt_status"]}','',f'**Try a related image brief:** [{v["related_label"]}]({v["related_prompt"]})','',f'Checked: {v["checked"]}. These related briefs are our suggestions, not the creator’s undisclosed prompt.','']
    (ROOT/'docs/x-videos.md').write_text('\n'.join(line.rstrip() for line in lines).rstrip()+'\n')
    print(f'Built {len(records)} source-linked video entries.')
if __name__=='__main__':build()
