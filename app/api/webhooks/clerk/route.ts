import { headers } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'
import { Webhook } from 'svix'

const webhookSecret = process.env.CLERK_WEBHOOK_SECRET || ''

async function handler(request: NextRequest) {
  if (!webhookSecret) {
    console.error('CLERK_WEBHOOK_SECRET is not set')
    return NextResponse.json({ error: 'Webhook secret not configured' }, { status: 500 })
  }

  // Get headers
  const headerPayload = headers()
  const svix_id = headerPayload.get('svix-id')
  const svix_timestamp = headerPayload.get('svix-timestamp')
  const svix_signature = headerPayload.get('svix-signature')

  // If there are no headers, error out
  if (!svix_id || !svix_timestamp || !svix_signature) {
    return NextResponse.json({ error: 'Missing svix headers' }, { status: 400 })
  }

  // Get body
  const payload = await request.text()

  // Create new Svix instance with secret
  const wh = new Webhook(webhookSecret)

  let evt: any

  // Verify payload with headers
  try {
    evt = wh.verify(payload, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    })
  } catch (err) {
    console.error('Error verifying webhook:', err)
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  // Handle the webhook
  const eventType = evt.type
  console.log(`Received webhook: ${eventType}`)

  try {
    // Forward the webhook to our backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const response = await fetch(`${backendUrl}/webhooks/clerk`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(evt),
    })

    if (!response.ok) {
      console.error('Backend webhook handler failed:', response.status, response.statusText)
      return NextResponse.json({ error: 'Backend processing failed' }, { status: 500 })
    }

    const result = await response.json()
    console.log('Webhook processed successfully:', result)

    return NextResponse.json({ success: true, message: 'Webhook processed' })
  } catch (error) {
    console.error('Error processing webhook:', error)
    return NextResponse.json({ error: 'Processing failed' }, { status: 500 })
  }
}

export const POST = handler
