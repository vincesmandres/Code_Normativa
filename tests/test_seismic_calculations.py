import pytest
from espectro_nec.seismic_calculations import parse_values, calculate_parameters, calculate_spectrum

def test_parse_values():
    class MockVar:
        def __init__(self, value):
            self.value = value
        def get(self):
            return self.value

    variables = {
        'zona_sismica_var': MockVar('I Zona'),
        'tipo_suelo_var': MockVar('A Suelo'),
        'region_var': MockVar('Costa'),
        'r_var': MockVar('3.0 Factor'),
        'i_var': MockVar('1.5 Factor')
    }
    result = parse_values(variables)
    assert result == ('I', 'A', 'Costa', 3.0, 1.5)

def test_calculate_parameters():
    params, eta, Z = calculate_parameters('A', 'I', 'Costa')
    assert params['Fa'] == 0.9
    assert params['Fd'] == 0.9
    assert params['Fs'] == 0.75
    assert params['r'] == 1
    assert eta == 1.8
    assert Z == 0.15

def test_calculate_spectrum():
    T, Sa, Se, Si, T0, Tc, TL = calculate_spectrum(0.15, 0.9, 0.9, 0.75, 1.8, 3.0, 1.5, 1.0, 1.0)
    assert len(T) == 1000
    assert Sa[0] == 0.15 * 0.9
    assert T0 == 0.1 * 0.75 * 0.9 / 0.9
    assert Tc == 0.55 * 0.75 * 0.9 / 0.9
    assert TL == 2.4 * 0.9