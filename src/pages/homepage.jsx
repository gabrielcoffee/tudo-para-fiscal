"use client"

import { useEffect, useState } from "react"
import "../styles/index.css"
import CountrySelector from "../components/CountrySelector";

import logo from "../assets/logotudopara.png";

export default function Home() {
const [numero, setNumero] = useState("");
const [numeroFormatado, setNumeroFormatado] = useState("");
const [numeroValido, setNumeroValido] = useState(false);
const [showAlert, setShowAlert] = useState(false);
const [selectedCountry, setSelectedCountry] = useState("Brasil")
const [placeholderNumber, setPlaceHolderNumber] = useState("(XX) XXXXX-XXXX");

useEffect(() => {
	if (selectedCountry === "Brasil") {
		setPlaceHolderNumber("(XX) XXXXX-XXXX")
	} else {
		setPlaceHolderNumber("(XXX) XXX-XXXX")
	}
}, [selectedCountry])

const numeros = [
	'5541998481062',
	'5541995154260',
	'5541995252470',
	'41995252470',
	'5544997027932',
	'5544997028415',
	'5541996170508',
];
  

const handleSubmit = () => {
	setShowAlert(true);

	if (numeros.includes(numero)) {
		setNumeroValido(true);
	}else {
		setNumeroValido(false);
	}

	if (numero.length === 11) {
		setNumeroFormatado(numero.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3"))
	} else if (numero.length === 0) {
		setNumeroFormatado("...")
	} else {
		setNumeroFormatado(numero.replace(/(\d{3})(\d{3})(\d{4})/, "($1) $2-$3"))
	}

}

return (
	<div className='min-h-screen flex flex-col custom-font-inter'>

	<main className="flex-grow flex items-center justify-center px-4 my-12">
		<div className="text-left max-w-5xl flex flex-col items-center gap-6">

		<img width={200} className="mb-8 mt-3" src={logo} alt="Logo da Tudo Para Fiscal"></img>

		<div className="text-center text-5xl text-[#2a2b28] text-balance">Verifique se um número faz parte da equipe oficial da <strong><span className="text-[#383a36] ">Tudo Para</span></strong></div>
	
		
		<div className="flex flex-col items-center">
			<CountrySelector selectedCountry={selectedCountry} setSelectedCountry={setSelectedCountry}/>
		</div>

		<div className="w-full max-w-md mx-auto">
			<div className="flex flex-col space-y-4 justify-center">
			<input
			maxLength={11}
				type="tel"
				placeholder={placeholderNumber}
				value={numero}
				onChange={(e) => setNumero(e.target.value)}
				className="text-lg bg-white/80 backdrop-blur-sm text-[#383a36] rounded-full px-6 py-3 border border-[#383a36]"
			/>
			<button
				onClick={handleSubmit}
				className="bg-[#383a36] hover:bg-[#191a19] text-white text-lg py-3 px-6 rounded-full transition-colors duration-300 hover:cursor-pointer"
			>
				Verificar
			</button>

			{
				showAlert ? (
					numeroValido ? (
						<div className="bg-green-400 p-4 rounded-sm shadow text-center">
						<span className="text-xl text-neutral-900 "><span className="font-bold">{numeroFormatado}</span> é um número Legítimo que faz parte da nossa equipe.</span>
						</div>
					) : (
						<div className="bg-red-400 p-4 rounded-sm shadow text-center">
						<span className="text-xl text-neutral-900 ">O número <span className="font-bold">{numeroFormatado}</span> NÃO faz parte de nossa equipe.</span>
						</div>
					)
				) :
				(null)
				
			}

			<ul className="list-disc text-left mx-6 pl-[40px] text-sm">
				<li>Preencha apenas com números;</li>
				<li>Lembre-se de incluir o DDD do Estado e o nono dígito;</li>
				<li>Não é necessário colocar o código do Brasil: +55 nem EUA: +1</li>
			</ul>

			<div className="text-center mt-12 flex flex-col">
				<span className="">Caso fique com dúvidas, <a href="https://www.tudoparafiscalecontrole.com.br/atendimento-wpp" className="font-bold underline hover:cursor-pointer">clique aqui</a> e fale com um dos nossos atendentes</span>
			</div>
			
			</div>
		</div>
		</div>
	</main>

	<footer className="bg-white/80 backdrop-blur-sm shadow">

		<div className="container mx-auto px-4 py-6 flex justify-between items-center">
		<div className="text-[#383a36]">© 2025 Tudo Para</div>
		<div className="flex flex-col space-y-2 md:space-y-0 md:space-x-8 md:flex-row">

				<a href="/politica-de-privacidade" className="text-left text-[#383a36] hover:text-[#151515]">
				Política de Privacidade
				</a>
				<a href="/termos-de-uso" className="text-left text-[#383a36] hover:text-[#151515]">
				Termos de Uso
				</a>

		</div>
		</div>

	</footer>

	

	<style jsx global>{`
		body {
		background-color: #fff;
		background-image: radial-gradient(circle at top left, rgba(6, 40, 70, 0.2) 0%, transparent 60%),
							radial-gradient(circle at bottom right, rgba(6, 40, 70, 0.2) 0%, transparent 60%);
		}
	`}</style>
	</div>
)
}

