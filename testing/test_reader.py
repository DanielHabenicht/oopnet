import unittest
import datetime

from oopnet.elements.enums import Unit, HeadlossFormula, BalancingOption, DemandModel, StatisticSetting, \
    ReportStatusSetting, ReportBoolSetting
from oopnet.elements import Junction, Tank, Reservoir, Pipe, Pump, Valve
from oopnet.simulator import Run
from oopnet.utils.getters import get_curve, get_pattern, get_patterns


class PoulakisEnhancedReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import PoulakisEnhancedPDAModel
        self.model = PoulakisEnhancedPDAModel()

    def test_junctions(self):
        self.assertEqual(self.model.n_junctions, len(self.model.network.junctions))
        for j in self.model.network.junctions.values():
            self.assertIsInstance(j, Junction)
            self.assertEqual(50, j.demand)
            self.assertTrue('J' in j.id)

    def test_tanks(self):
        self.assertEqual(self.model.n_tanks, len(self.model.network.tanks))
        for t in self.model.network.tanks.values():
            self.assertIsInstance(t, Tank)
            self.assertEqual(50, t.diam)
            self.assertTrue('J' in t.id)

    def test_reservoirs(self):
        self.assertEqual(self.model.n_reservoirs, len(self.model.network.reservoirs))
        for r in self.model.network.reservoirs.values():
            self.assertIsInstance(r, Reservoir)
            self.assertEqual(52, r.head)
            self.assertTrue('J' in r.id)

    def test_pipes(self):
        self.assertEqual(self.model.n_pipes, len(self.model.network.pipes))
        for p in self.model.network.pipes.values():
            self.assertIsInstance(p, Pipe)
            self.assertEqual(0.26, p.roughness)
            self.assertTrue(p.diameter in [600, 450, 300])
            self.assertTrue('P' in p.id)

    def test_pumps(self):
        self.assertEqual(self.model.n_pumps, len(self.model.network.pumps))
        for p in self.model.network.pumps.values():
            self.assertIsInstance(p, Pump)
            self.assertEqual('HEAD', p.keyword)
            self.assertTrue('P' in p.id)

    def test_valves(self):
        self.assertEqual(self.model.n_valves, len(self.model.network.valves))
        for v in self.model.network.valves.values():
            self.assertIsInstance(v, Valve)
            self.assertEqual(500, v.diameter)
            self.assertTrue('P' in v.id)

    def test_curves(self):
        c1 = get_curve(self.model.network, '1')
        self.assertEqual([50, 100], c1.xvalues)
        self.assertEqual([5, 10], c1.yvalues)

        c2 = get_curve(self.model.network, '2')
        self.assertEqual([50], c2.xvalues)
        self.assertEqual([50], c2.yvalues)

        c3 = get_curve(self.model.network, '3')
        self.assertEqual([2, 5], c3.xvalues)
        self.assertEqual([20, 50], c3.yvalues)

    def test_options(self):
        options = self.model.network.options
        self.assertEqual(Unit.LPS, options.units)
        self.assertEqual(40, options.trials)
        self.assertEqual(HeadlossFormula.DW, options.headloss)
        self.assertEqual(1.00000004749745E-10, options.accuracy)
        self.assertEqual(1, options.demandmultiplier)
        self.assertEqual(1, options.emitterexponent)
        self.assertEqual(1, options.pattern)
        self.assertEqual(DemandModel.PDA, options.demandmodel)
        self.assertEqual(0, options.minimumpressure)
        self.assertEqual(10, options.requiredpressure)
        self.assertEqual(0.5, options.pressureexponent)
        self.assertEqual((BalancingOption.CONTINUE, 10), options.unbalanced)
        self.assertEqual(1, options.viscosity)
        self.assertEqual(1.00000004749745E-10, options.tolerance)

    def test_report(self):
        report = self.model.network.report
        self.assertEqual(ReportStatusSetting.FULL, report.status)
        self.assertEqual(ReportBoolSetting.NO, report.summary)

    def test_times(self):
        times = self.model.network.times
        self.assertEqual(datetime.timedelta(hours=0), times.duration)
        self.assertEqual(datetime.timedelta(hours=1), times.hydraulictimestep)
        self.assertEqual(datetime.timedelta(minutes=5), times.qualitytimestep)
        self.assertEqual(datetime.timedelta(hours=1), times.patterntimestep)
        self.assertEqual(datetime.timedelta(), times.patternstart)
        self.assertEqual(datetime.timedelta(hours=1), times.reporttimestep)
        self.assertEqual(datetime.timedelta(), times.reportstart)
        self.assertEqual(datetime.timedelta(), times.startclocktime)
        self.assertEqual(StatisticSetting.NONE, times.statistic)

    def test_run(self):
        Run(self.model.network)

    # todo: add options, reportparameter, curve, pattern ... tests


class MicorpolisReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import MicropolisModel
        self.model = MicropolisModel()

    def test_controls(self):
        self.assertEqual(self.model.n_controls, len(self.model.network.controls))

    def test_rules(self):
        self.assertEqual(self.model.n_rules, len(self.model.network.rules))

    def test_patterns(self):
        self.assertEqual(self.model.n_patterns, len(self.model.network.patterns))
        for pat in get_patterns(self.model.network):
            self.assertEqual(24, len(pat.multipliers))

        p = get_pattern(self.model.network, '3')
        self.assertEqual([0.96, 0.96, 0.96, 0.96, 1.06, 1.07, 1.06, 0.96, 0.96, 0.96, 0.96, 0.96, 1.065, 1.075, 1.056,
                          0.96, 0.96, 0.96, 0.96, 0.96, 1.065, 1.075, 1.065, 0.96], p.multipliers)

    def test_run(self):
        Run(self.model.network)

    def test_options(self):
        options = self.model.network.options
        self.assertEqual(Unit.LPS, options.units)
        self.assertEqual(40, options.trials)
        self.assertEqual(HeadlossFormula.DW, options.headloss)
        self.assertEqual(0.001, options.accuracy)
        self.assertEqual(1, options.demandmultiplier)
        self.assertEqual(0.5, options.emitterexponent)
        defpat = get_pattern(self.model.network, 'DefPat')
        self.assertEqual(defpat, options.pattern)
        self.assertEqual(DemandModel.DDA, options.demandmodel)
        self.assertEqual(None, options.minimumpressure)
        self.assertEqual(None, options.requiredpressure)
        self.assertEqual(None, options.pressureexponent)
        self.assertEqual((BalancingOption.CONTINUE, 10), options.unbalanced)
        self.assertEqual(1, options.viscosity)
        self.assertEqual(0.01, options.tolerance)

    def test_report(self):
        report = self.model.network.report
        self.assertEqual(ReportStatusSetting.NO, report.status)
        self.assertEqual(ReportBoolSetting.NO, report.summary)

    def test_times(self):
        times = self.model.network.times
        self.assertEqual(datetime.timedelta(hours=240), times.duration)
        self.assertEqual(datetime.timedelta(hours=1), times.hydraulictimestep)
        self.assertEqual(datetime.timedelta(minutes=5), times.qualitytimestep)
        self.assertEqual(datetime.timedelta(hours=1), times.patterntimestep)
        self.assertEqual(datetime.timedelta(), times.patternstart)
        self.assertEqual(datetime.timedelta(hours=1), times.reporttimestep)
        self.assertEqual(datetime.timedelta(), times.reportstart)
        self.assertEqual(datetime.timedelta(), times.startclocktime)
        self.assertEqual(StatisticSetting.NONE, times.statistic)


class RulesModelReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import RulesModel
        self.model = RulesModel()

    def test_options(self):
        options = self.model.network.options
        self.assertEqual(Unit.LPS, options.units)
        self.assertEqual(40, options.trials)
        self.assertEqual(HeadlossFormula.HW, options.headloss)
        self.assertEqual(0.001, options.accuracy)
        self.assertEqual(1, options.demandmultiplier)
        self.assertEqual(0.5, options.emitterexponent)
        self.assertEqual(1, options.pattern)
        self.assertEqual(DemandModel.DDA, options.demandmodel)
        self.assertEqual(None, options.minimumpressure)
        self.assertEqual(None, options.requiredpressure)
        self.assertEqual(None, options.pressureexponent)
        self.assertEqual((BalancingOption.CONTINUE, 10), options.unbalanced)
        self.assertEqual(1, options.viscosity)
        self.assertEqual(0.01, options.tolerance)

    def test_run(self):
        self.assertEqual(DemandModel.DDA, self.model.network.options.demandmodel)
        Run(self.model.network)

    def test_rules(self):
        self.assertEqual(self.model.n_rules, len(self.model.network.rules))


class CTownReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import CTownModel
        self.model = CTownModel()

    def test_run(self):
        rpt = Run(self.model.network, delete=False)


if __name__ == '__main__':
    unittest.main()
