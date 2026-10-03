-- RailForge: 20 estacoes, 4 linhas e 20 conexoes para o mapa.
-- Requer as tabelas criadas pela API. Nao remove dados existentes.
BEGIN;

DO $$
DECLARE
    mock_line RECORD;
    line_id INTEGER;
    station_id INTEGER;
    station_sequence INTEGER;
BEGIN
    -- Os nomes reservados permitem detectar uma carga anterior sem fixar IDs.
    IF EXISTS (
        SELECT 1 FROM line
        WHERE name IN ('MOCK - Azul', 'MOCK - Verde', 'MOCK - Vermelha', 'MOCK - Amarela')
    ) OR EXISTS (
        SELECT 1 FROM station WHERE description = 'RailForge mock: 20 estacoes / 4 linhas'
    ) THEN
        RAISE EXCEPTION 'Mock ja cadastrado ou nomes reservados em uso. Nenhum dado foi inserido.';
    END IF;

    FOR mock_line IN
        SELECT * FROM (VALUES
            ('MOCK - Azul', '#2563eb', 100, ARRAY['Central', 'Mercado', 'Biblioteca', 'Universidade', 'Terminal Norte']),
            ('MOCK - Verde', '#16a34a', 200, ARRAY['Jardim', 'Parque', 'Bosque', 'Lago', 'Terminal Sul']),
            ('MOCK - Vermelha', '#dc2626', 300, ARRAY['Fabrica', 'Oficinas', 'Estadio', 'Hospital', 'Terminal Leste']),
            ('MOCK - Amarela', '#eab308', 400, ARRAY['Museu', 'Teatro', 'Praca', 'Prefeitura', 'Terminal Oeste'])
        ) AS data(name, color, position_y, station_names)
    LOOP
        INSERT INTO line (name, color)
        VALUES (mock_line.name, mock_line.color)
        RETURNING id INTO line_id;

        FOR station_sequence IN 1..5 LOOP
            INSERT INTO station (name, description, position_x, position_y)
            VALUES (
                'MOCK - ' || mock_line.station_names[station_sequence],
                'RailForge mock: 20 estacoes / 4 linhas',
                station_sequence * 100,
                mock_line.position_y
            )
            RETURNING id INTO station_id;

            INSERT INTO conection (id_station, id_line, sequence)
            VALUES (station_id, line_id, station_sequence);
        END LOOP;
    END LOOP;
END;
$$;

COMMIT;
