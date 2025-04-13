# Dimenzió Processzorok

A dimenzió processzorok különböző piaci aspektusokat (dimenziókat) elemző komponensek,
amelyek strukturált eredményeket adnak vissza a további feldolgozáshoz vagy vizualizációhoz.

## D1 - Alap adatok (Base Data)
### Komponensek
```python
{
    'timeframes': ['M1', 'M5', 'M15', 'H1', 'H4', 'D1'],
    'values': {
        'price': ['open', 'high', 'low', 'close'],
        'volume': ['tick_volume'],
        'spread': ['spread'],
        'real_volume': ['real_volume']
    }
}
```

### Függvények
- `_process_implementation(data, timeframe)`: Alapadatok feldolgozása

### Visszatérési értékek
```python
{
    'weight': float,  # Időkeret súly
    'mt5_data': {
        'open': Series,    # Nyitó árak
        'high': Series,    # Maximum árak
        'low': Series,     # Minimum árak
        'close': Series,   # Záró árak
        'tick_volume': Series,  # Tick volumen
        'spread': Series,       # Spread értékek
        'real_volume': Series    # Valós volumen
    }
}
```

## D2 - Support/Resistance szintek
### Komponensek
```python
{
    'timeframes': {
        'major': ['D1', 'H4', 'H1'],
        'minor': ['M15', 'M5', 'M1']
    },
    'config': {
        'swing_threshold': 0.001,     # Swing pont küszöb
        'level_merge': 0.002,         # Szint összevonási küszöb
        'min_candles': 5,             # Minimum gyertyák száma
        'strength_window': 100,       # Erősség számítás ablak
        'use_close_open': true,       # Záró/nyitó árak használata (elsődleges)
        'use_high_low': true,         # High/low értékek használata (másodlagos)
        'primary_weight': 0.7,        # Elsődleges (záró/nyitó) súlyozás
        'secondary_weight': 0.3,      # Másodlagos (high/low) súlyozás
        'volume_confirmation': true,  # Volumen megerősítés használata
        'min_touches': 2              # Minimum érintések száma
    }
}
```

### Függvények
- `_find_swing_points_close_open(df)`: Swing pontok keresése záró/nyitó árak alapján
- `_find_swing_points_high_low(df)`: Swing pontok keresése high/low értékek alapján
- `_identify_levels(df, swing_points, level_type)`: Szintek azonosítása
- `_merge_levels(levels)`: Közeli szintek összevonása
- `_confirm_with_volume(df, levels)`: Szintek megerősítése volumen alapján
- `_calculate_level_strength(df, level, window)`: Szint erősségének számítása
- `_categorize_zones(df, levels)`: Zónák kategorizálása


### Visszatérési értékek
```python
{
    'weight': float,
    'support_levels': List[Dict],  # Support szintek és erősségük
    'resistance_levels': List[Dict],  # Resistance szintek és erősségük
    'swing_points': {
        'swing_highs': numpy.ndarray,  # Boolean maszk
        'swing_lows': numpy.ndarray    # Boolean maszk
    },
    'zones': {
        'support': {
            'strong': List[Dict],    # Erős support szintek
            'moderate': List[Dict],  # Közepes support szintek
            'weak': List[Dict]       # Gyenge support szintek
        },
        'resistance': {
            'strong': List[Dict],    # Erős resistance szintek
            'moderate': List[Dict],  # Közepes resistance szintek
            'weak': List[Dict]       # Gyenge resistance szintek
        }
    }
}
```

## D3 - Trend komponensek
### Komponensek
```python
{
    'trend': {
        'short_window': 20,     # Rövid MA ablak
        'long_window': 50,      # Hosszú MA ablak
        'smooth_factor': 0.1,   # EMA simítási faktor
        'threshold': 0.02,      # Trend váltási küszöb
        'consolidation_threshold': 0.01,  # Konszolidációs küszöb
        'ma_type': 'ema'        # MA típus (ema, sma, wma)
    }
}
```

### Függvények
- `_calculate_ma(df, window, ma_type)`: Mozgóátlag számítása (EMA, SMA, WMA)
- `_calculate_trend_direction(df, short_ma, long_ma)`: Trend irány számítása
- `_calculate_trend_strength(df, direction, short_ma, long_ma)`: Trend erősség számítása
- `_calculate_trend_duration(direction)`: Trend időtartam számítása
- `_detect_trend_changes(direction)`: Trend változások detektálása
### Visszatérési értékek
```python
{
    'weight': float,
    'trend': {
        'direction': Series,    # -1 (short), 0 (konsz), 1 (long)
        'strength': Series,     # 0-1 közötti erősség
        'duration': Series,     # Trend időtartam
        'changes': Series,      # Trend változások (0, ±0.1, ±0.5, ±1.0)
        'short_ma': Series,     # Rövid MA
        'long_ma': Series,      # Hosszú MA
        'params': {
            'short_window': int,  # Rövid MA ablakméret
            'long_window': int,   # Hosszú MA ablakméret
            'ma_type': str,       # MA típus
            'threshold': float,   # Trend küszöb
            'consolidation_threshold': float  # Konszolidációs küszöb
        }
    }
}
```

## D4 - Mozgóátlag komponensek
### Komponensek
```python
{
    'moving_averages': {
        'windows': [20, 50, 100, 200],
        'types': ['sma', 'ema', 'wma', 'hull'],
        'price_type': 'close',
        'cross_threshold': 0.001,
        'ribbon_threshold': 0.002
    }
}
```

### Függvények
- `_calculate_moving_averages(df, windows, ma_types, price_type)`: MA-k számítása különböző típusokkal és ablakméretekkel
- `_detect_crossovers(moving_averages, threshold)`: Kereszteződések detektálása
- `_calculate_ma_features(moving_averages, df, ribbon_threshold)`: MA jellemzők számítása

### Visszatérési értékek
```python
{
    'weight': float,
    'moving_averages': {
        'sma': {
            20: Series,   # 20 periódusos SMA
            50: Series,   # 50 periódusos SMA
            100: Series,  # 100 periódusos SMA
            200: Series   # 200 periódusos SMA
        },
        'ema': {
            # ... EMA értékek
        },
        'wma': {
            # ... WMA értékek
        },
        'hull': {
            # ... Hull MA értékek
        }
    },
    'crossovers': {
        'sma': {
            '20-50': DataFrame({  # 20-50 SMA kereszteződés
                'prev_state': Series,   # Előző állapot (0/1)
                'curr_state': Series,   # Jelenlegi állapot (0/1)
                'cross_up': Series,     # Felfelé kereszteződés (0/1)
                'cross_down': Series,   # Lefelé kereszteződés (0/1)
                'strength': Series,     # Kereszteződés erősség
                'is_significant': Series  # Jelentős-e a kereszteződés
            }),
            # ... további kereszteződések
        },
        # ... további MA típusok kereszteződései
    },
    'features': {
        'sma': {
            'price_to_ma_20': Series,   # Ár és 20 SMA távolsága
            'price_above_ma_20': Series, # Ár 20 SMA felett (0/1)
            'ribbon_width': Series,     # MA szalag szélesség
            'ribbon_aligned_up': Series, # MA-k felfelé mutatnak (0/1)
            'ribbon_aligned_down': Series, # MA-k lefelé mutatnak (0/1)
            'ribbon_converging': Series, # MA-k közelednek (0/1)
            'ribbon_diverging': Series,  # MA-k távolodnak (0/1)
            'trend_strength_20': Series, # 20 SMA trend erőssége
            # ... további jellemzők
        },
        # ... további MA típusok jellemzői
    }
}
```

## D5 - Momentum komponensek
### Komponensek
```python
{
    'timeframes': ['M5', 'M15', 'H1', 'H4'],
    'config': {
        'rsi_period': 14,
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        'stoch_k_period': 14,
        'stoch_d_period': 3
    },
    'weights': {
        'M5': 0.3,
        'M15': 0.5,
        'H1': 0.8,
        'H4': 1.0
    }
}
```

### Függvények
- `calculate_rsi(df, period, price_col)`: RSI számítása
- `calculate_macd(df, fast, slow, signal, price_col)`: MACD számítása
- `calculate_stochastic(df, k_period, d_period, price_cols)`: Stochastic számítása
- `detect_overbought_oversold(rsi, stoch_k, stoch_d)`: Túlvett/túladott állapotok detektálása
- `detect_divergence(price_series, indicator, type_)`: Divergenciák detektálása
- `detect_macd_cross(macd, signal, type_)`: MACD kereszteződések detektálása
- `detect_momentum_reversal(series, direction)`: Momentum irányváltások detektálása
- `calculate_momentum_strength(rsi, macd_histogram, stochastic_k)`: Momentum erősség számítása

### Visszatérési értékek
```python
{
    'weight': float,  # Időkeret súly
    'indicators': {
        'rsi': pd.Series,  # RSI értékek
        'macd': {
            'macd': pd.Series,  # MACD vonal
            'signal': pd.Series,  # Signal vonal
            'histogram': pd.Series  # MACD histogram
        },
        'stochastic': {
            '%K': pd.Series,  # Stochastic %K
            '%D': pd.Series  # Stochastic %D
        }
    },
    'signals': {
        'overbought_oversold': pd.DataFrame,  # Túlvett/túladott jelzések
        'divergences': {
            'rsi_bullish_divergence': pd.Series,
            'rsi_bearish_divergence': pd.Series,
            'macd_bullish_divergence': pd.Series,
            'macd_bearish_divergence': pd.Series,
            'stoch_bullish_divergence': pd.Series,
            'stoch_bearish_divergence': pd.Series
        },
        'momentum_signals': {
            'bullish_cross': pd.Series,  # MACD bullish kereszteződés
            'bearish_cross': pd.Series,  # MACD bearish kereszteződés
            'momentum_reversal_up': pd.Series,  # Felfelé irányváltás
            'momentum_reversal_down': pd.Series,  # Lefelé irányváltás
            'stoch_reversal_up': pd.Series,  # Stochastic felfelé irányváltás
            'stoch_reversal_down': pd.Series  # Stochastic lefelé irányváltás
        }
    },
    'features': {
        'momentum_strength': pd.Series  # Kombinált momentum erősség (0-1)
    }
}
```

## D6 - Fibonacci szintek
### Komponensek
```python
{
    'fibonacci': {
        'retracements': [
            {
                'price': float,      # Zóna középső ára
                'upper': float,      # Zóna felső határa
                'lower': float,      # Zóna alsó határa
                'strength': float,   # Zóna erősség (0-1)
                'type': str,         # 'strong', 'moderate', 'weak'
                'touches': int,      # Érintések száma
                'levels': [          # A zónát alkotó szintek
                    {
                        'level': float,  # Fibonacci szint (0.618, stb.)
                        'type': str,     # 'retracement' vagy 'extension'
                        'price': float,  # Konkrét árszint
                        'source': {      # Forrás információ
                            'start_time': datetime,
                            'end_time': datetime
                        }
                    }
                ]
            }
        ],
        'extensions': [
            # Ugyanaz a struktúra mint a retracement zónáknál
        ],
        'harmonics': [
            {
                'type': str,         # 'ABCD', 'Butterfly', 'Gartley', stb.
                'direction': str,    # 'bullish' vagy 'bearish'
                'points': {          # Mintázat pontjai
                    'A': {'index': int, 'time': datetime, 'price': float},
                    'B': {'index': int, 'time': datetime, 'price': float},
                    'C': {'index': int, 'time': datetime, 'price': float},
                    'D': {'index': int, 'time': datetime, 'price': float},
                    # Komplex mintázatoknál 'X' is
                },
                'ratios': {          # Fibonacci arányok
                    'ab_bc': float,
                    'bc_cd': float,
                    # Komplex mintázatoknál több arány
                },
                'quality': float,    # Mintázat minősége (0-1)
                'entry': float,      # Belépési ár
                'stop': float,       # Stop loss ár
                'target': float,     # Célár
                'risk_reward': float,  # Kockázat/nyereség arány
                'completion': float   # A mintázat teljesültségi szintje (0-1)
            }
        ],
        'price_targets': {  # Ártargetek
            'targets': {
                'above': [  # Ár feletti targetek
                    {
                        'price': float,
                        'strength': float,
                        'type': str,
                        'source': str,
                        'distance': float
                    }
                ],
                'below': [  # Ár alatti targetek
                    # Ugyanaz a struktúra mint az 'above' targeteknél
                ]
            },
            'resistance_levels': [float, ...],  # Ellenállás szintek
            'support_levels': [float, ...],     # Támasz szintek
            'recommended': {  # Ajánlott ártargetek
                'resistance': float,
                'support': float,
                'risk_reward': {
                    'long': {
                        'risk_reward': float,
                        'stop_loss': float,
                        'take_profit': float
                    },
                    'short': {
                        'risk_reward': float,
                        'stop_loss': float,
                        'take_profit': float
                    },
                    'recommended': str  # 'long' vagy 'short'
                }
            }
        }
    }
}
```

### Függvények
- `_identify_swing_points(df, config)`: Swing pontok azonosítása (high/low vagy close árak alapján)
- `_identify_significant_swings(df, swing_highs, swing_lows, lookback, min_strength)`: Legfontosabb swing pontok keresése
- `_calculate_retracements(df, swing_points, config)`: Fibonacci visszahúzódási szintek számítása
- `_calculate_extensions(df, swing_points, config)`: Fibonacci kiterjesztési szintek számítása
- `_identify_harmonic_patterns(df, swing_points, config)`: Harmonikus mintázatok azonosítása
- `_find_abcd_patterns(swings, min_quality)`: ABCD harmonikus mintázatok keresése
- `_find_harmonic_patterns(swings, pattern_types, min_quality)`: Komplex harmonikus mintázatok keresése
- `_validate_and_strengthen_zones(df, levels, level_type)`: Zónák validálása és erősség számítása
- `_count_zone_touches(df, zone)`: Zóna érintések száma
- `_calculate_price_targets(df, retrace_zones, ext_zones)`: Ártarget számítás
- `_calculate_risk_reward(curr_price, res_target, supp_target)`: Kockázat/nyereség számítás

### Visszatérési értékek
```python
{
    'weight': float,  # Processzor súlya
    'swing_points': {
        'swing_highs': np.ndarray,  # Boolean maszk a high pontokra
        'swing_lows': np.ndarray,   # Boolean maszk a low pontokra
        'significant_swings': [      # Kulcsfontosságú swing pontok
            {
                'index': int,        # Index a DataFrame-ben
                'time': datetime,    # Időbélyeg
                'price': float,      # Árszint
                'type': str,         # 'high' vagy 'low'
                'strength': float    # Swing erősség (0-1)
            }
        ]
    },
    'fibonacci': {
        'retracements': [  # Fibonacci visszahúzódási zónák
            {
                'price': float,      # Zóna központi ár
                'upper': float,      # Zóna felső határ
                'lower': float,      # Zóna alsó határ
                'strength': float,   # Zóna erősség (0-1)
                'type': str,         # 'strong', 'moderate', 'weak'
                'touches': int,      # Érintések száma
                'levels': [          # A zónát alkotó szintek
                    {
                        'level': float,  # Fibonacci szint (0.618, stb.)
                        'type': str,     # 'retracement' vagy 'extension'
                        'price': float,  # Konkrét árszint
                        'source': {      # Forrás információ
                            'start_time': datetime,
                            'end_time': datetime
                        }
                    }
                ]
            }
        ],
        'extensions': [  # Fibonacci kiterjesztési zónák
            # Ugyanaz a struktúra mint a retracement zónáknál
        ],
        'harmonics': [  # Harmonikus mintázatok
            {
                'type': str,         # 'ABCD', 'Butterfly', 'Gartley', stb.
                'direction': str,    # 'bullish' vagy 'bearish'
                'points': {          # Mintázat pontjai
                    'A': {'index': int, 'time': datetime, 'price': float},
                    'B': {'index': int, 'time': datetime, 'price': float},
                    'C': {'index': int, 'time': datetime, 'price': float},
                    'D': {'index': int, 'time': datetime, 'price': float},
                    # Komplex mintázatoknál 'X' is
                },
                'ratios': {          # Fibonacci arányok
                    'ab_bc': float,
                    'bc_cd': float,
                    # Komplex mintázatoknál több arány
                },
                'quality': float,    # Mintázat minősége (0-1)
                'entry': float,      # Belépési ár
                'stop': float,       # Stop loss ár
                'target': float,     # Célár
                'risk_reward': float,  # Kockázat/nyereség arány
                'completion': float   # A mintázat teljesültségi szintje (0-1)
            }
        ],
        'price_targets': {  # Ártargetek
            'targets': {
                'above': [  # Ár feletti targetek
                    {
                        'price': float,
                        'strength': float,
                        'type': str,
                        'source': str,
                        'distance': float
                    }
                ],
                'below': [  # Ár alatti targetek
                    # Ugyanaz a struktúra mint az 'above' targeteknél
                ]
            },
            'resistance_levels': [float, ...],  # Ellenállás szintek
            'support_levels': [float, ...],     # Támasz szintek
            'recommended': {  # Ajánlott ártargetek
                'resistance': float,
                'support': float,
                'risk_reward': {
                    'long': {
                        'risk_reward': float,
                        'stop_loss': float,
                        'take_profit': float
                    },
                    'short': {
                        'risk_reward': float,
                        'stop_loss': float,
                        'take_profit': float
                    },
                    'recommended': str  # 'long' vagy 'short'
                }
            }
        }
    }
}
```

## D7 - Gyertyaformációk
### Komponensek
```python
{
    'candlesticks': {
        'body_threshold': 0.001,    # Test/árnyék arány küszöb
        'pattern_window': 5,        # Formáció keresési ablak
        'volume_confirm': True,     # Volumen megerősítés használata
        'min_pattern_size': 0.002   # Minimum formáció méret
    }
}
```

### Függvények
- `identify_single_patterns(df)`: Egyedi gyertyaminták
- `identify_double_patterns(df)`: Kettős gyertyaminták
- `identify_triple_patterns(df)`: Hármas gyertyaminták
- `calculate_pattern_strength(df, patterns)`: Formáció erősség

### Visszatérési értékek
```python
{
    'weight': float,
    'patterns': {
        'single': Dict,    # Egyedi minták
        'double': Dict,    # Kettős minták
        'triple': Dict     # Hármas minták
    },
    'quality': Dict       # Formáció minőség
}
```

## D8 - Chart mintázatok
### Komponensek
```python
{
    'timeframes': ['M15', 'H1', 'H4', 'D1'],
    'config': {
        'min_pattern_length': 5,          # Minimum pontok száma egy mintázathoz
        'max_pattern_length': 50,         # Maximum pontok száma egy mintázathoz
        'min_pattern_significance': 0.01,  # Minimum árváltozás a mintázatban (az átlagos napi tartomány százalékában)
        'min_pattern_quality': 0.7,       # Minimum mintázat minőség (0-1)
        'linear_regression_samples': 50,  # Lineáris regresszióhoz használt pontok száma
        'trend_strength_threshold': 0.6,  # Trend erősség küszöb a trendvonalakhoz
        'breakout_confirmation_bars': 2,  # Kitörés megerősítéséhez szükséges gyertyák
        'swing_point_threshold': 0.01,    # Swing pontok azonosításához használt küszöbérték
        'volume_confirmation': true,      # Volumen megerősítés használata
        'risk_reward_min': 1.5,           # Minimum kockázat/nyereség arány
        'pattern_height_significance': 0.01  # Mintázat magasság minimum (ár százalékában)
    }
}
```

### Függvények
- `_identify_swing_points(data)`: Swing (fordulópont) pontok azonosítása
- `_find_head_and_shoulders(data, swing_highs, swing_lows)`: Fej-váll mintázatok felismerése
- `_find_double_pattern(data, swing_highs, swing_lows, pattern_type)`: Dupla tető/alj mintázatok felismerése
- `_find_triple_pattern(data, swing_highs, swing_lows, pattern_type)`: Tripla tető/alj mintázatok felismerése
- `_find_triangle_patterns(data, swing_highs, swing_lows)`: Háromszög mintázatok felismerése
- `_find_flag_pattern(data, swing_highs, swing_lows)`: Zászló mintázatok felismerése
- `_identify_trendlines(data, swing_points)`: Trendvonalak és csatornák azonosítása
- `_detect_reversal_patterns(data, swing_points)`: Trend megfordulási mintázatok azonosítása
- `_detect_continuation_patterns(data, swing_points)`: Trend folytatódási mintázatok azonosítása
- `_analyze_breakouts(data, patterns)`: Kitörések elemzése
- `_generate_trading_opportunities(data, patterns, breakouts)`: Kereskedési lehetőségek generálása

### Visszatérési értékek
```python
{
    'weight': float,            # Az időkeret súlyozása
    'patterns': {
        'reversal': {           # Trend megfordulási minták
            'head_and_shoulders': {
                'type': str,        # 'head_and_shoulders' vagy 'inverse_head_and_shoulders'
                'direction': str,   # 'bullish' vagy 'bearish'
                'quality': float,   # Mintázat minőség (0-1)
                'start_index': int, # Kezdő index
                'end_index': int,   # Végző index
                'points': {         # Kulcsfontosságú pontok
                    'left_shoulder': int,
                    'head': int,
                    'right_shoulder': int,
                    'neckline': [int, int]
                },
                'breakout_level': float,   # Kitörési szint
                'pattern_height': float,   # Mintázat magasság
                'price_target': float,     # Ártarget
                'reliability': float       # Megbízhatóság (0-1)
            },
            'double_top': {},   # Hasonló struktúra
            'double_bottom': {},  # Hasonló struktúra
            'triple_top': {},   # Hasonló struktúra
            'triple_bottom': {}  # Hasonló struktúra
        },
        'continuation': {      # Trend folytatódási minták
            'symmetrical_triangle': {},  # Háromszögek
            'ascending_triangle': {},
            'descending_triangle': {},
            'flag': {},        # Zászló mintázatok
            'pennant': {}      # Zászlócska mintázatok
        },
        'trendlines': {        # Trendvonalak és csatornák
            'support': [        # Support trendvonalak
                {
                    'slope': float,
                    'intercept': float,
                    'r_value': float,      # Regresszió R² érték
                    'points': [int, ...],  # Trendvonal pontjai
                    'direction': str       # 'up' vagy 'down'
                }
            ],
            'resistance': [     # Resistance trendvonalak
                # Hasonló struktúra mint a support trendvonalaknál
            ],
            'channels': [       # Azonosított csatornák
                {
                    'type': str,           # 'ascending_channel', 'descending_channel', 'horizontal_channel'
                    'upper_trendline': dict,  # Felső trendvonal (lásd fent)
                    'lower_trendline': dict,  # Alsó trendvonal (lásd fent)
                    'width': float,           # Csatorna szélesség
                    'direction': str          # Csatorna irány
                }
            ]
        }
    },
    'breakouts': [             # Azonosított kitörések
        {
            'pattern_type': str,         # Mintázat típusa
            'pattern_quality': float,    # Mintázat minőség
            'direction': str,            # Kitörés iránya
            'breakout_status': str,      # 'confirmed' vagy 'potential'
            'volume_confirmed': bool,    # Volumen megerősítés
            'price_target': float,       # Ártarget
            'risk_reward_ratio': float,  # Kockázat/nyereség arány
            'reliability': float,        # Megbízhatóság
            'timestamp': datetime        # Kitörés időbélyege
        }
    ],
    'opportunities': [         # Kereskedési lehetőségek
        {
            'type': str,               # 'breakout_trade' vagy 'pattern_formation'
            'pattern_type': str,       # Mintázat típusa
            'direction': str,          # 'bullish' vagy 'bearish'
            'entry_price': float,      # Belépési ár (vagy potenciális belépési ár)
            'target_price': float,     # Célár (vagy potenciális célár)
            'risk_reward_ratio': float, # Kockázat/nyereség arány
            'reliability': float,      # Megbízhatóság
            'timestamp': datetime,     # Időbélyeg
            'description': str         # Szöveges leírás
        }
    ],
    'swing_points': {          # Azonosított swing pontok
        'swing_highs': np.ndarray,  # Boolean maszk a swing high pontokra
        'swing_lows': np.ndarray    # Boolean maszk a swing low pontokra
    }
}
```

## D9 - Volume Flow
### Komponensek
```python
{
    'timeframes': ['M15', 'H1', 'H4', 'D1'],
    'config': {
        'delta_window': 14,          # Delta számítás ablak
        'volume_threshold': 1.5,     # Volume spike azonosítás küszöb
        'zone_threshold': 0.2,       # Zóna azonosítás árváltozás küszöb
        'control_threshold': 0.6,    # Kontroll érték küszöb nyomás elemzéshez
        'pressure_lookback': 20,     # Nyomás számítás visszatekintési periódus
        'min_zone_size': 5           # Minimum zóna méret gyertyákban
    }
}
```

### Függvények
```python
- `_calculate_volume_delta(data)`: Volume delta számítás (vételi és eladási erők különbsége)
- `_analyze_pressure(data, delta)`: Piaci nyomás elemzése (trend erősség és irány meghatározása)
- `_identify_volume_zones(data, delta)`: Akkumulációs és disztribúciós zónák azonosítása
- `_detect_volume_patterns(data, delta)`: Volume mintázatok felismerése (kiugró volumen, divergenciák)
```
### Visszatérési értékek
```python
{
    'weight': float,                  # Az időkeret súlyozása
    'delta': {                        # Volumen különbözeti mutatók
        'volume_delta': pd.Series,     # Nyers delta értékek
        'cumulative_delta': pd.Series, # Kumulatív delta
        'delta_sma': pd.Series,        # Delta mozgóátlag
        'normalized_delta': pd.Series  # Normalizált delta
    },
    'pressure': {                     # Piaci nyomás indikátorok
        'buy_sell_pressure': pd.Series,  # Vételi-eladási nyomás egyensúly (-1 és 1 között)
        'control': pd.Series,            # Kontroll érték (0-1 között, magas = egyensúly)
        'buyer_control': pd.Series,      # Vevői kontroll boolean maszk
        'seller_control': pd.Series,     # Eladói kontroll boolean maszk
        'uptrend_pressure': pd.Series,   # Emelkedő trend nyomás boolean maszk
        'downtrend_pressure': pd.Series, # Csökkenő trend nyomás boolean maszk
        'balanced_pressure': pd.Series   # Egyensúlyi nyomás boolean maszk
    },
    'zones': {                        # Azonosított volumen zónák
        'accumulation': List[Dict],     # Akkumulációs zónák
        'distribution': List[Dict],      # Disztribúciós zónák
        'neutral': List[Dict]            # Semleges zónák
    },
    'patterns': {                     # Felismert volumen mintázatok
        'volume_climax': List[Dict],     # Volumen csúcs események
        'volume_divergence': List[Dict], # Ár-volumen divergenciák
        'absorption': List[Dict]         # Abszorpciós mintázatok
    },
    'metrics': {                      # Volumen metrikák
        'avg_volume': pd.Series,         # Átlagos volumen (20 gyertya)
        'volume_change': pd.Series,      # Volumen változás
        'relative_volume': pd.Series,    # Relatív volumen (az 50 napos átlaghoz képest)
        'volume_trend': pd.Series        # Volumen trend iránya
    }
}
```

## D10 - Volatilitás és Range
### Komponensek
```python
{
    'volatility': {
        'timeframes': ['M1', 'M5', 'M15', 'H1'],
        'atr_periods': {
            'short': 14,
            'medium': 21,
            'long': 50
        },
        'band_settings': {
            'bollinger': {
                'periods': 20,
                'std_dev': 2.0
            },
            'keltner': {
                'periods': 20,
                'atr_mult': 1.5
            }
        }
    }
}
```

### Függvények
- `calculate_atr(df, period)`: ATR számítása
- `calculate_bands(df)`: Bollinger és Keltner sávok
- `calculate_regime(df, atr)`: Volatilitás rezsim
- `calculate_risk_params(df, atr)`: Kockázati paraméterek

### Visszatérési értékek
```python
{
    'weight': float,
    'indicators': {
        'atr': Dict,     # ATR értékek
        'bands': Dict    # Sávok
    },
    'state': Dict,       # Volatilitás rezsim
    'risk': Dict        # Kockázati paraméterek
}
```

## D11 - Piaci környezet
### Komponensek
```python
{
    'context': {
        'timeframes': ['M1', 'M5', 'M15', 'H1'],
        'sessions': {
            'asian': {'start': time(0, 0), 'end': time(8, 0)},
            'london': {'start': time(8, 0), 'end': time(16, 0)},
            'new_york': {'start': time(13, 0), 'end': time(21, 0)}
        },
        'liquidity': {
            'spread_thresholds': {
                'tight': 0.0002,   # 2 pips
                'wide': 0.0005     # 5 pips
            },
            'volume_percentiles': {
                'high': 80,
                'low': 20
            }
        }
    }
}
```

### Függvények
- `analyze_session(df)`: Piaci szakaszok elemzése
- `analyze_liquidity(df)`: Likviditás állapot elemzése
- `analyze_market_type(df)`: Piaci típus és erősség

### Visszatérési értékek
```python
{
    'weight': float,
    'session': {
        'type': Dict,      # Session típusok
        'overlap': Dict,   # Átfedések
        'activity': Dict   # Aktivitás szintek
    },
    'liquidity': Dict,     # Likviditási állapot
    'market_type': Dict    # Piaci kondíció
}
```

## D12 - Order Flow
### Komponensek
```python
{
    'order_flow': {
        'timeframes': ['M1', 'M5', 'M15', 'H1'],
        'momentum': {
            'delta_period': 14,
            'acceleration_period': 5
        },
        'liquidity': {
            'cluster_threshold': 0.0002,  # 2 pips
            'volume_threshold': 0.8       # 80%-os volumen szint
        },
        'pressure': {
            'imbalance_period': 20,
            'absorption_threshold': 0.7
        }
    }
}
```

### Függvények
- `analyze_imbalance(df)`: Piaci egyensúlytalanság
- `analyze_momentum(df)`: Momentum és delta változások
- `analyze_levels(df)`: Likviditási szintek

### Visszatérési értékek
```python
{
    'weight': float,
    'imbalance': {
        'pressure': Dict,    # Vételi/eladási nyomás
        'absorption': Dict   # Abszorpció állapotok
    },
    'momentum': {
        'delta': Dict,        # Delta értékek
        'acceleration': Dict  # Változás gyorsulás
    },
    'levels': {
        'liquidity': Dict,    # Likviditási poolok
        'orders': Dict        # Order klaszterek
    }
}
```

## D13 - Divergencia
### Komponensek
```python
{
    'divergence': {
        'lookback': {
            'price': 20,
            'indicator': 14,
            'volume': 30
        },
        'thresholds': {
            'angle': 15.0,       # Minimális divergencia szög
            'distance': 0.002    # Minimális ár távolság
        },
        'rsi_params': {
            'period': 14,
            'overbought': 70,
            'oversold': 30
        }
    }
}
```

### Függvények
- `analyze_price_divergence(df)`: Ár divergenciák
- `analyze_indicator_divergence(df)`: Indikátor divergenciák
- `analyze_volume_divergence(df)`: Volume divergenciák

### Visszatérési értékek
```python
{
    'weight': float,
    'price': {
        'regular': Dict,     # Reguláris divergenciák
        'hidden': Dict,      # Rejtett divergenciák
        'strength': Dict     # Divergencia erősség
    },
    'indicators': Dict,      # Indikátor divergenciák
    'volume': Dict          # Volume divergenciák
}
```

## D14 - Kitörések
### Komponensek
```python
{
    'break': {
        'min_distance': 0.001,     # Minimum kitörési távolság
        'volume_mult': 1.5,        # Volumen megerősítés szorzó
        'momentum_thresh': 0.002,   # Momentum küszöb
        'speed_window': 5          # Kitörés sebesség ablak
    },
    'retest': {
        'return_thresh': 0.7,      # Visszatérési minimum
        'reaction_strength': 0.003, # Reakció erősség küszöb
        'quality_window': 10       # Minőség vizsgálati ablak
    },
    'continuation': {
        'prob_window': 20,         # Valószínűség ablak
        'target_mult': 2.0,        # Célár szorzó
        'min_probability': 0.6     # Minimum folytatási valószínűség
    }
}
```

### Függvények
- `analyze_break_quality(df)`: Kitörés minőség
- `analyze_retest(df)`: Visszatesztelések
- `analyze_continuation(df)`: Folytatódás elemzés

### Visszatérési értékek
```python
{
    'weight': float,
    'quality': Dict,       # Kitörés minőség
    'retest': Dict,        # Visszatesztelés jellemzők
    'continuation': Dict   # Folytatódás valószínűség
}
```

## D15 - Kockázatkezelés
### Komponensek
```python
{
    'risk': {
        'position': {
            'max_risk_percent': 0.02,    # Maximum 2% kockázat
            'volatility_factor': 0.5,    # Volatilitás korrekció
            'trend_factor': 0.3         # Trend erősség korrekció
        },
        'stops': {
            'atr_factor': 1.5,          # ATR szorzó
            'structure_min_distance': 20  # Minimum pip távolság
        },
        'targets': {
            'min_rr_ratio': 1.5,        # Minimum R/R arány
            'optimal_rr_ratio': 2.5,     # Optimális R/R arány
            'partial_exit_level': 0.618  # Fibonacci kilépési szint
        }
    }
}
```

### Függvények
- `calculate_position_size(df)`: Pozícióméret számítás
- `calculate_stops(df)`: Stop loss távolságok
- `calculate_targets(df)`: Profit célok
- `calculate_exposure(df)`: Kitettség limitek

### Visszatérési értékek
```python
{
    'weight': float,
    'position': {
        'calculation': Dict,  # Méret számítások
        'adjustment': Dict    # Korrekciós faktorok
    },
    'stops': {
        'initial': Dict,     # Kezdeti stopok
        'trailing': Dict     # Trailing stopok
    },
    'targets': Dict,         # Profit célok
    'exposure': Dict         # Kitettség limitek
}
