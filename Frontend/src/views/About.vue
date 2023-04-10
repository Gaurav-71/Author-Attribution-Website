<template>
  <div class="about-page pa-5 pt-10">
    <div class="text-h4 mt-2 cyan--text">
      Development and Analysis of Real-time Computational Linguistic Algorithms
      for Authorship Prediction on Indian Regional Languages
    </div>
    <p class="mt-6">
      Authorship prediction is one of the popular applications of Natural
      language processing. It is a task of predicting the probability of a true
      author of an anonymous text based on his/her writing style. Kannada being
      one of the popular south Indian languages is lagging in this domain. It is
      the state language of Karnataka and spoken by more than 50 million people
      around the globe. The language has a rich set of vocabulary, grammar and
      literature. Text processing on many Indian regional languages is
      progressing highly but in Kannada, it is still in a tender stage. The
      proposed work mainly focuses on predicting the authorship of an unknown
      Kannada text based on the Stylometry features.
    </p>
    <div class="approaches">
      <div v-for="(approach, index) in approaches" :key="index">
        <Card :data="approach" />
      </div>
    </div>
    <div class="text-h4 cyan--text">Societal impact</div>
    <p class="mt-6">
      The proposed work will be contributed to Karnataka Ganaka Parishath a
      voluntary organization contributed in the area of Kannada text processing.
      KAGAPA has contributed voluminous dataset for the proposed work. KAGAPA
      will be utilizing this tool to resolve any authorship issues in literature
      in future. The entire work will be automated and developed as an
      application tool and will be released for the public to use it.
    </p>
    <div class="text-h4 cyan--text mt-8">Author & Supervisor</div>
    <div class="professors mt-8">
      <div v-for="(professor, index) in professors" :key="index">
        <ProfessorCard :data="professor" />
      </div>
    </div>
    <div class="bottom-space mt-15"></div>
  </div>
</template>

<script>
import Card from "../components/design/Card.vue";
import ProfessorCard from "../components/design/ProfessorCard.vue";
export default {
  components: { Card, ProfessorCard },
  data() {
    return {
      approaches: [
        {
          imgName: "profile",
          title: "Profile based approach",
          description:
            "Extracted Lexical features like frequency of words/ character/ nouns/pronouns/ word pair and then classified using various classification algorithms",
        },
        {
          imgName: "lstm",
          title: "Bi-directional LSTM technique",
          description:
            "Syntactic features like POS tags are extracted and classified using LSTM network",
        },
        {
          imgName: "instance",
          title: "Instance based approach",
          description:
            "Extracted syntactic features using word and char –N grams and classified using various classification algorithms",
        },
        {
          imgName: "compression",
          title: "Compression based approach",
          description:
            "Applied Zip, Gzip, Bzip, LZMA and PPmd compression algorithms to predict the probability of a true author.",
        },
        {
          imgName: "graph",
          title: "Graph based approach",
          description:
            "Representing the author and their articles as a connected graph then extracting the character and word N-gram features and perform the classification using convolution neural network.",
        },
      ],
      professors: [
        {
          imgName: "chandrika",
          name: "Mrs. Chandrika Prasad",
          role: "Author",
          designation:
            "Research Scholar in the Dept. of Computer Science & Engineering",
          college: "Ramaiah Institute of Technology",
        },
        {
          imgName: "jaggi",
          role: "Supervisor",
          name: "Dr. Jagadish Kallimani",
          designation:
            "Professor & Head of Artificial Intelligence & Machine Learning",
          college: "Ramaiah Institute of Technology",
        },
      ],
    };
  },
};
</script>

<style lang="scss" scoped>
.approaches {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  margin: 2rem 0;
  flex-wrap: wrap;
}
.professors {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}
</style>