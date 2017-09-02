from sphinxwrapper import *
import time


def main():
    ps1 = PocketSphinx()  # JSGF decoder
    ps2 = PocketSphinx()  # LM decoder

    # Set up decoder 1 with a JSGF grammar
    grammar = """
    #JSGF V1.0 UTF-8 en;
    grammar g;
    public <greet> = hi <name>;
    <name> = peter | john | mary | anna;
    """
    ps1.set_jsgf_search(grammar)
    hyp = None
    
    def jsgf_hyp_callback(s):
        print("JSGF hypothesis: %s" % s)
        global hyp
        hyp = s

    def lm_hyp_callback(s):
        print("Language model hypothesis: %s" % s)
        global hyp
        hyp = s

    def speech_start_callback():
        print("Speech started.")

    ps1.hypothesis_callback = jsgf_hyp_callback
    ps2.hypothesis_callback = lm_hyp_callback
    ps1.speech_start_callback = speech_start_callback
    ps2.speech_start_callback = speech_start_callback
    
    # Recognise from the mic in a loop
    ps1.open_rec_from_audio_device()
    ps1.start_utterance()  # must do this before processing audio
    recorded_audio = []
    while True:
        audio = ps1.read_audio()
        ps1.process_audio(audio)
        recorded_audio.append(audio)
        global hyp
        if hyp:
            break
        time.sleep(0.1)

    # Reprocess the recorded audio with a different decoder
    print("Reprocessing...")
    ps2.start_utterance()
    for a in recorded_audio:
        ps2.process_audio(a)

if __name__ == "__main__":
    main()
