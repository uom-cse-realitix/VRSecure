import simpleaudio as sa


wave_obj = sa.WaveObject.from_wave_file("./data/alarm_sound.wav")

play_obj = wave_obj.play()

play_obj.stop()
play_obj.wait_done()