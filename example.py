"""
示例脚本 - 演示如何使用 Paper2Reader
"""
from workflow import Paper2ReaderWorkflow
from utils import save_note

# 示例论文内容
example_paper = """
Title: Attention Is All You Need

Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin

Abstract:
The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show that these models are superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature.

1. Introduction
Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation. Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures.

2. Background
The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU, ByteNet and ConvS2S, all of which use convolutional neural networks as basic building block, computing hidden representations in parallel for all input and output positions.

3. Model Architecture
Most competitive neural sequence transduction models have an encoder-decoder structure. Here, the encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence of continuous representations z = (z1, ..., zn). Given z, the decoder then generates an output sequence (y1, ..., ym) of symbols one element at a time.

4. Experiments
We trained the base models on the WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs. Sentences were encoded using byte-pair encoding, which has a shared source-target vocabulary of about 37000 tokens.

5. Conclusion
In this work, we proposed the Transformer, the first sequence transduction model based entirely on attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.
"""


def main():
    """运行示例"""
    print("=" * 60)
    print("Paper2Reader 示例")
    print("=" * 60)
    
    # 创建工作流
    print("\n初始化工作流...")
    workflow = Paper2ReaderWorkflow()
    
    # 处理论文
    print("\n开始处理论文...")
    result = workflow.run(example_paper)
    
    if result.get('success'):
        # 获取笔记内容
        note_content = result.get('note_content', '')
        
        # 保存笔记
        output_path = save_note(note_content, 'outputs/example_note.md')
        print(f"\n✅ 处理完成！笔记已保存到: {output_path}")
        
        # 显示质量评分
        quality_check = result.get('quality_check', {})
        if isinstance(quality_check, dict):
            completeness = quality_check.get('completeness_score', 0)
            accuracy = quality_check.get('accuracy_score', 0)
            clarity = quality_check.get('clarity_score', 0)
            
            print(f"\n质量评分:")
            print(f"  完整性: {completeness:.2f}")
            print(f"  准确性: {accuracy:.2f}")
            print(f"  清晰度: {clarity:.2f}")
    else:
        print(f"\n❌ 处理失败: {result.get('error', '未知错误')}")


if __name__ == '__main__':
    main()
