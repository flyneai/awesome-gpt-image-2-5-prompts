"""Render substantive homepage examples from the canonical prompt/source records."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
def sections(lang):
    zh=lang=='zh';recipes={r['id']:r for r in read('data/prompts.json')['core']}
    assets={a['recipe_id']:a for a in read('assets/manifest.json')['assets'] if a.get('role') not in ('input','draft')}
    why={
      'P092':('A bakery campaign with room for final copy. Separate bread texture, hands and a blank strip instead of asking the image to invent an offer.','适合面包店广告。把面包纹理、手部与留白分开说明，再用排版工具添加准确的活动文案。'),
      'P093':('A travel-journal cover built around a paper window. The physical paper edge and the miniature scene need separate material descriptions.','适合旅行手账封面。纸张开口和窗口里的微缩场景采用不同的材质描述，避免整幅图都变成平面插画。'),
      'P094':('A fictional aerial landscape for a mood board. Specify the spiral as shoreline geometry, then explain water-depth color without inventing a real location.','适合景观灵感图。把螺旋写成岸线形状，再说明水深与颜色的关系；这不是实际地点或地理资料。')}
    reviews={'P092':'示例中可见三份面包与留白条；双手部分遮挡，使用前需检查手指与接触位置。','P093':'可见纸张纤维和城镇；竖版画面中的开口偏宽，建筑为虚构，不代表真实目的地。','P094':'潟湖与沙洲形成宽螺旋，外侧有植被和礁石细节；地形为虚构。'}
    lines=['<a id="homepage-examples"></a>', '', '## 三个完整案例：看效果、复制、再修改' if zh else '## Three complete examples: inspect, copy, refine','',
      '以下三例均有独立生成图片。示例来自内置图片工具，未返回底层模型编号，不作为 Flyne 平台或特定模型的效果实测。初次生成不用参考图；后续修改须上传自己确认的结果。' if zh else 'Each example below has a separately generated image. The built-in image tool did not expose its model ID; these are not verified Flyne platform or named-model tests. Start from text, then upload your approved result for the separate next edit.','']
    for rid in ['P092','P093','P094']:
        r=recipes[rid];a=assets[rid];source=r['source_reference'];preview='assets/previews/'+Path(a['path']).with_suffix('.jpg').name
        lines += ['### '+rid+' · '+r['title'][lang],'',why[rid][int(zh)],'',f'[![{a["alt"]}]({preview})]({a["path"]})','',
          (f'**输入与比例：** 无参考图，{r["ratio"]}。复制下面的完整提示词，替换自己的商品或场景。' if zh else f'**Input and ratio:** no reference image, {r["ratio"]}. Copy the complete prompt; replace the subject or setting to suit your brief.'),'','```text',r['prompt'][lang],'```','',
          '**确认第一张图后，再单独修改：** 上传确认稿，然后使用下方指令。' if zh else '**After approving the first image:** upload that version and run this edit separately.','','```text',r['revision'][lang],'```','',
          ('**检查示例：** '+reviews[rid] if zh else '**Example review:** '+r['review']['en']),'',
          (f'**来源与记录：** 灵感来自 [{source["handle"]}]({source["url"]})；上面的图片是本库改写后的独立示例，不是作者原图。[实际执行提示词]({a["prompt_path"]}) · [完整配方与改写说明](prompts/{r["pack"]}.md#{rid.lower()})。' if zh else f'**Source and record:** inspired by [{source["handle"]}]({source["url"]}). The image above is this library’s independently generated adaptation, not the source author’s image. [Exact executed prompt]({a["prompt_path"]}) · [Recipe and adaptation notes](prompts/{r["pack"]}.md#{rid.lower()}).'),'']
    videos=read('data/x-videos.json')['videos']
    vlines=['<a id="homepage-videos"></a>', '', '## 从图片到视频：三个来源案例与操作示范' if zh else '## From stills to video: three creator references and a working brief','',
      '点击封面在 X 播放原帖。下列模型分工来自作者说明；已核对原帖文字、播放器和封面，未独立核验模型，也未审查完整播放，作者未公开完整提示词。GPT Image 2.5 用于静态图，运动由另一视频工具完成。外部媒体不纳入本库 MIT 许可，原帖或预览可能失效。' if zh else 'Click each poster to watch the original on X. Model roles come from the authors: post text, player and poster were inspected; model identities were not independently verified, and full playback was not audited and complete prompts were not published. GPT Image 2.5 supplies stills; another tool supplies motion. External media is outside the repository’s MIT license; posts or previews may become unavailable.','']
    for v in videos:
        title=v['title'].split(' · ')[int(zh)];summary=v['summary'].split(' / ')[int(zh)];link=v['related_prompt'].removeprefix('../')
        vlines += ['### '+v['id']+' · '+title,'',f'[![{title}]({v["poster_url"]})]({v["url"]})','',summary,'',
           (f'**作者与工具：** [{v["author"]}（{v["handle"]}）]({v["url"]})；静态图：{v["image_model"]}；视频：{v["video_model"]}。核对日期：{v["checked"]}。' if zh else f'**Creator and tools:** [{v["author"]} ({v["handle"]})]({v["url"]}); stills: {v["image_model"]}; video: {v["video_model"]}. Checked {v["checked"]}.'),'',
           (f'[可借用的静态图配方]({link})：这是本库建议的起点，并非作者未公开的原提示词。' if zh else f'[Related still-image recipe]({link}): our suggested starting point, not the creator’s unpublished prompt.'),'']
    motions=re.findall(r'```text\n(.*?)\n```',(ROOT/'docs/image-to-video-workflow.md').read_text(),re.S)
    vlines += ['### 自己做一次：让 P092 面包广告轻微推进' if zh else '### Try the workflow: a subtle push-in on the P092 bakery image','',
       '**本库编写的模板，尚未完成视频实测。** 不冒充上述作者的原提示词。' if zh else '**Authored here; video output has not been tested.** This is not a reconstruction of any creator’s unpublished prompt.','',
       '1. 使用本页 P092 的完整提示词生成静态图，检查三份面包、手部和留白，保存确认稿。\n2. 把确认稿上传到支持图生视频的工具，先查看价格和可用时长；图片免费入口不代表视频免费。\n3. 若支持五秒，使用下方指令；否则同时修改工具时长和指令。\n4. 完整播放结果，检查首尾帧、手指、面包数量、文字变形和闪烁。保留准确提示词、输入图、模型显示名称与输出，不满意就回到确认稿重试。' if zh else '1. Generate the still with the complete P092 prompt on this page. Check the three breads, hands and blank strip; save your approved version.\n2. Upload it into a tool supporting image-to-video. Check price and available duration first; free image access does not establish free video access.\n3. If five seconds is supported, use the motion brief below. Otherwise change both the selected duration and prompt.\n4. Watch the entire output, including first and last frames. Check fingers, loaf count, warped lettering and flicker. Save the exact prompt, input, displayed model name and result; retry from the approved still if needed.','',
       '```text',motions[int(zh)],'```','',
       '**控制变化：** 第一次只动镜头，不同时加入手部动作、面包转动和场景切换。文字需要严格准确时，留白生图、后期排字，比让视频持续重绘小字更容易验收。' if zh else '**Control the change:** begin with camera motion alone. Do not simultaneously add hand movement, rotating bread and scene cuts. For exact typography, generate with blank space and add text in post-production so you can verify it separately.','',
       '[来源与权利记录](docs/x-videos.md) · [完整操作指南](docs/image-to-video-workflow.md)' if zh else '[Source and rights records](docs/x-videos.md) · [Workflow guide](docs/image-to-video-workflow.md)','']
    return {'HOMEPAGE EXAMPLES':'\n'.join(lines).rstrip(),'HOMEPAGE VIDEOS':'\n'.join(vlines).rstrip()}
