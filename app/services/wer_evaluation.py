import jiwer

_transform = jiwer.Compose([
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(),
])


def evaluate_wer(reference: str, hypothesis: str) -> dict:
    """
    WER = (S + D + I) / N
    S: Substitution, D: Deletion, I: Insertion, N: 정답(reference) 단어 수
    """

    output = jiwer.process_words(
        reference,
        hypothesis,
        reference_transform=_transform,
        hypothesis_transform=_transform,
    )

    S = output.substitutions
    D = output.deletions
    I = output.insertions
    H = output.hits

    N = S + D + H

    wer = (S + D + I) / N if N > 0 else 0.0

    return {
        "S": S,
        "D": D,
        "I": I,
        "N": N,
        "wer": wer,
    }
