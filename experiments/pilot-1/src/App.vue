<template>
  <Experiment title="Plurals in Context: A Language Study">
    <InstructionScreen :title="'Welcome'">
      <p>Thank you for taking part in our experiment! The session will take approximately 10-15 minutes.</p>

      <p><strong>About the Study:</strong><br />
      This study investigates language use in context. You will evaluate visual scenes paired with sentences by indicating their acceptability on a slider. Your responses will contribute to our understanding of language processing in varied scenarios. More details about the research questions will be provided upon completion of the experiment. Detailed instructions and practice trials will follow on the next screen.</p>

      <p><strong>Participation Information:</strong><br />
      Your participation is entirely voluntary. You can discontinue the experiment at any point without any negative consequences. Please respond naturally and try not to overthink your ratings.</p>

      <p><strong>Data Collection:</strong><br />
      All data collected is completely anonymised and will be used solely for research purposes.</p>
    </InstructionScreen>

    <InstructionScreen>
      <p><strong>Instructions:</strong></p>
      <p>In each trial, you will be presented with a visual scene paired with a sentence. Your task is to evaluate how well the sentence fits the context shown in the image. Use the slider to indicate your level of acceptability, then click the "Submit" button to proceed to the next trial.</p>
      <!-- <p>You will have the opportunity to take a break after completing half of the trials.</p> -->
    </InstructionScreen>

    <InstructionScreen>
      <p><strong>Practice Trials:</strong></p>
      <p>For each practice trial, you will see a visual scene paired with a sentence. Use the slider to indicate your level of acceptability, then click the "Submit" button to proceed to the next trial.</p>
      <p>Let's start with the first practice trial.</p>
    </InstructionScreen>

    <template v-for="(trial, i) in practiceTrials">
      <Screen :key="i"
              :progress="i / practiceTrials.length">
        <!-- Display trial content (customize as needed) -->
        <img :src="getImagePath(trial.List,trial.itemNr)" />
        <p>{{ trial.linguisticContext }}</p>
            <!-- <br>
            F1 NP: {{trial.F1_NPforms}}
            <br>
            F2 matchness: {{trial.F2_matchness}}
            <br>
            List: {{trial.List}}
            <br>
            Item number: {{trial.itemNr}}
            <br>
            Groupby: {{trial.Grouped}} -->
        <SliderInput
          left="completely unacceptable"
          right="completely acceptable"
          :response.sync="$magpie.measurements.practice" />
          {{$magpie.measurements.practice}}
        <button v-if="$magpie.measurements.practice" @click="$magpie.saveAndNextScreen();">
          Submit
        </button>
        <Record
            :data="{
              trialNR: i,
              itemNr: trial.itemNr,
              List: trial.List,
              F1_NPforms: trial.F1_NPforms,
              F2_matchness: trial.F2_matchness,
              acceptability: $magpie.measurements.practice,
            }"
          />
      </Screen>
    </template>

    <InstructionScreen>
      <p><strong>You're Ready to Begin!</strong></p>
      <p>The main experiment trials are about to start.</p>
      <p>Please respond naturally and avoid overthinking your ratings.</p>
    </InstructionScreen>

    <template v-for="(trial, i) in mainTrials">
      <Screen
            :key="i"
            :progress="i / mainTrials.length">
            <img :src="getImagePath(trial.List,trial.itemNr)" />

            {{trial.linguisticContext}}
            <br>
            <!-- F1 NP: {{trial.F1_NPforms}}
            <br>
            F2 matchness: {{trial.F2_matchness}}
            <br>
            List: {{trial.List}}
            <br>
            Item number: {{trial.itemNr}}
            <br>
            Groupby: {{trial.Grouped}} -->


            <SliderInput
            left="completely unacceptable"
            right="completely acceptable"
            :response.sync= "$magpie.measurements.acceptability" />
            {{$magpie.measurements.acceptability}}
            <button v-if="$magpie.measurements.acceptability" @click="$magpie.saveAndNextScreen();">Submit</button>
            <Record
            :data="{
              trialNR: i,
              itemNr: trial.itemNr,
              List: trial.List,
              F1_NPforms: trial.F1_NPforms,
              F2_matchness: trial.F2_matchness,
              acceptability: $magpie.measurements.acceptability,
            }"
          />
        </Slide>
        </Screen>
    </template>
    <InstructionsScreen>
      <p>Thank you for participating in our experiment!</p>
      <p>Your responses have been recorded.</p>
      <p>Please click the button below to submit your results.</p>
    </InstructionsScreen>
    <PostTestScreen />
    <SubmitResultsScreen />


  </Experiment>
</template>

<script>
import _ from 'lodash';
import allItems from '../trials/items.csv'

export default {
  name: 'App',
  data() {
    return {
      // Choose a random list between 1 and 6 (computed once at creation)
      randomList: _.sample([1, 2, 3, 4, 5, 6]),
      // Manual mode toggle and manual list value (null means no override)
      manualMode: false,
      manualList: null
    };
  },
  computed: {
    // Expose lodash to template code
    _() {
      return _;
    },
    // Determine which list to use: manual or random
    activeList() {
      return this.manualMode && this.manualList ? this.manualList : this.randomList;
    },
    // Create a computed property 'items' for the filtered and shuffled trials
    items() {
      // Assumes each item in the CSV has a property named "list"
      return _.shuffle(
        allItems.filter(item => Number(item.List) === Number(this.activeList))
      );
    },
    practiceTrials() {
      return this.items.filter(trial => trial.itemNr >= 801 && trial.itemNr <= 803);
    },
    mainTrials() {
      return this.items.filter(trial => trial.itemNr < 801 || trial.itemNr > 803);
    },
  },
  methods: {
    getImagePath(list, itemNr) {
      return require(`../pictures/img_l${list}_i${itemNr}.svg`);
    }
  }
};
</script>
