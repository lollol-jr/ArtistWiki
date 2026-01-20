export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">
          ArtistWiki
        </h1>
        <p className="text-center text-lg mb-4">
          작가/예술가 위키 시스템
        </p>
        <p className="text-center text-sm text-gray-600">
          미디어위키 + AI 에이전트 오케스트레이션
        </p>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-3 lg:text-left gap-4">
        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100">
          <h2 className="mb-3 text-2xl font-semibold">
            미술가
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            화가, 조각가 등 시각예술가 정보
          </p>
        </div>

        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100">
          <h2 className="mb-3 text-2xl font-semibold">
            작가
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            소설가, 시인 등 문학가 정보
          </p>
        </div>

        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100">
          <h2 className="mb-3 text-2xl font-semibold">
            음악가
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            작곡가, 연주자 등 음악가 정보
          </p>
        </div>
      </div>
    </main>
  )
}
