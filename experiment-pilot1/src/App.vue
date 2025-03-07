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
import items from '../trials/items_test.csv'

export default {
  name: 'App',
  data() {
    return {
      items: _.shuffle(items),
      //items: items
      //random choose items.List
      //items: _.sample(items.map(item => item.List)),
      //items: _.sample(this.items.map(item => item.List)),
      //items: items.filter(item => item.List === 1)
    };
  },
  computed: {
    // Expose lodash to template code
    _() {
      return _;
    }
  },
  methods: {
    getImagePath(list, itemNr) {
      return require(`../pictures/img_l${list}_i${itemNr}.svg`);
    }
  }
};
</script>
