from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer

# Initialize disambiguators
mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
mle_egy = MLEDisambiguator.pretrained('calima-egy-r13')


# We expect a sentence to be whitespace/punctuation tokenized beforehand.
# We provide a simple whitespace and punctuation tokenizer as part of camel_tools.
# See camel_tools.tokenizers.word.simple_word_tokenize.
sentence_msa = ['فمن']
sentence_egy = ['فمن']

# Create different morphological tokenizer instances
msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok')
msa_atb_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='atbtok')
msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok')
egy_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_egy, scheme='d3tok')

# Generate tokenizations
# Note that our Egyptian resources currently provide bwtok tokenization only.
msa_d3_tok = msa_d3_tokenizer.tokenize(sentence_msa)
msa_atb_tok = msa_atb_tokenizer.tokenize(sentence_msa)
msa_bw_tok = msa_bw_tokenizer.tokenize(sentence_msa)
egy_d3_tok = egy_d3_tokenizer.tokenize(sentence_egy)
# Print results
print('D3 tokenization (MSA):', msa_d3_tok)
print('ATB tokenization (MSA):', msa_atb_tok)
print('BW tokenization (MSA):', msa_bw_tok)
print('D3 tokenization (EGY):', egy_d3_tok)