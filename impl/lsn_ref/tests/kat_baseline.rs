use lsn_ref::{
    ToyKemParams, toy_kat_vector, toy_wrong_secret_control, toy_wrong_secret_control_to_json,
};

#[test]
fn toy_kat_vector_roundtrips_with_zero_noise() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let kat = toy_kat_vector(params, 0xA11CE, 0x5EED, 0xC0DE, 0xBEEF);

    assert_eq!(kat.encapsulated_key_hex, kat.decapsulated_key_hex);
    assert_eq!(kat.ciphertext_syndrome_bits.len(), params.polar_n);
    assert_eq!(kat.message_bits.len(), params.polar_k);
}

#[test]
fn toy_kat_vector_detects_wrong_secret_negative_control() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };

    let control = toy_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0x5EED, 0xC0DE, 0xBEEF);

    assert_eq!(
        control.honest.encapsulated_key_hex,
        control.honest.decapsulated_key_hex
    );
    assert_ne!(
        control.honest.encapsulated_key_hex,
        control.wrong_secret_decapsulated_key_hex
    );
    assert!(!control.wrong_secret_roundtrip_ok);
}

#[test]
fn toy_wrong_secret_control_json_records_both_outcomes() {
    let params = ToyKemParams {
        n: 2,
        sample_count: 64,
        repetition: 3,
        polar_n: 16,
        polar_k: 8,
        public_noise_rate: 0.0,
        decoder_design_p: 0.0343,
    };
    let control = toy_wrong_secret_control(params, 0xA11CE, 0xA11CF, 0x5EED, 0xC0DE, 0xBEEF);
    let json = toy_wrong_secret_control_to_json("codex-lsn-ref-toy-kat", &control);

    assert!(json.contains("\"roundtrip_ok\": true"));
    assert!(json.contains("\"wrong_secret_roundtrip_ok\": false"));
    assert!(json.contains("\"status\": \"toy reference KAT scaffold"));
}
