<template>
  <Experiment title="magpie demo">
    <InstructionScreen :title="'Welcome'">
      This is a sample introduction screen.
    </InstructionScreen>
    <template v-for="(trial, i) in items">
      <Screen
            :key="i">
            <img :src="getImagePath(trial.List,trial.itemNr)" />

            {{trial.linguisticContext}}
            <br>
            F1 NP: {{trial.F1_NPforms}}
            <br>
            F2 matchness: {{trial.F2_matchness}}
            <br>
            List: {{trial.List}}
            <br>
            Item number: {{trial.itemNr}}
            <br>
            Groupby: {{trial.Grouped}}


            <SliderInput
            left="very unacceptable"
            right="very acceptable"
            :response.sync= "$magpie.measurements.acceptability" />
            {{$magpie.measurements.acceptability}}
            <button v-if="$magpie.measurements.acceptability" @click="$magpie.saveAndNextScreen();">Submit</button>
            <Record
            :data="{
              trialNR: i,
              itemNr: trial.itemNr,
              List: trial.List,
              F1: trial.F1_NPforms,
              F2: trial.F2_matchness,
              acceptability: $magpie.measurements.acceptability,
            }"
          />
        </Slide>
        </Screen>
    </template>
    <SubmitResultsScreen />
  </Experiment>
</template>

<script>
import _ from 'lodash';
import allItems from '../trials/items_test.csv'

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
    }
  },
  methods: {
    getImagePath(list, itemNr) {
      return require(`../pictures/img_l${list}_i${itemNr}.svg`);
    }
  }
};
</script>
